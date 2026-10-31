"""Comprobaciones sin pesos: adaptación de conversación y aislamiento por sesión."""
from contextlib import nullcontext
import json
from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch

NOTEBOOK = Path(__file__).resolve().parents[1] / "Blue_IA_Experimento_001.ipynb"


class Tokens:
    def __init__(self, length):
        self.shape = (1, length)
        self.device = None

    def to(self, device):
        self.device = device
        return self


class Tokenizer:
    eos_token_id = 99

    def __init__(self):
        self.messages = []
        self.last_tokens = None

    def apply_chat_template(self, messages, **kwargs):
        self.messages = [dict(m) for m in messages]
        self.last_tokens = Tokens(sum(len(m['content']) for m in messages))
        return self.last_tokens

    def decode(self, tokens, **kwargs):
        return 'respuesta de prueba'


class Output:
    def __getitem__(self, key):
        return []


class Model:
    def __init__(self):
        self.calls = []
        self.fail = False

    def parameters(self):
        return iter([SimpleNamespace(device='cpu')])

    def generate(self, **kwargs):
        if self.fail:
            raise RuntimeError('error interno')
        self.calls.append(kwargs)
        return Output()


class Updates:
    @staticmethod
    def update(**kwargs):
        return kwargs


class WebNotebookTests(TestCase):
    @classmethod
    def setUpClass(cls):
        notebook = json.loads(NOTEBOOK.read_text(encoding='utf-8'))
        cells = {cell['id']: ''.join(cell['source']) for cell in notebook['cells']}
        cls.web_source = cells['blue-web-05']
        cls.ui_source = cells['blue-web-07']
        cls.launch_source = cells['blue-web-09']

    def setUp(self):
        self.tokenizer = Tokenizer()
        self.model = Model()
        self.torch = SimpleNamespace(inference_mode=nullcontext, ones_like=lambda t: t)
        self.env = {'modelo': self.model, 'tokenizador': self.tokenizer}
        with patch.dict('sys.modules', {'torch': self.torch, 'gradio': Updates}):
            exec(compile(self.web_source, 'web_cell', 'exec'), self.env)

    def test_multiple_turns_form_correct_template_and_do_not_duplicate(self):
        generate = self.env['generar_respuesta_web']
        _, first = generate('primera', [])
        _, second = generate('segunda', first)
        messages = self.tokenizer.messages
        self.assertEqual([m['role'] for m in messages], ['system', 'user', 'assistant', 'user'])
        self.assertEqual(messages[0]['content'], self.env['PERSONALIDAD_WEB'])
        self.assertEqual([m['content'] for m in messages[1:]], ['primera', 'respuesta de prueba', 'segunda'])
        self.assertEqual(len(first), 2)
        self.assertEqual(len(second), 4)
        self.assertEqual(self.model.calls[-1]['input_ids'].device, 'cpu')
        self.assertEqual(self.model.calls[-1]['max_new_tokens'], 128)
        self.assertFalse(self.model.calls[-1]['do_sample'])

    def test_sessions_are_separate_and_reset_only_one(self):
        respond = self.env['responder_web']
        a = list(respond('mensaje A', []))[-1][1]
        b = list(respond('mensaje B', []))[-1][1]
        self.assertEqual(a[0]['content'], 'mensaje A')
        self.assertEqual(b[0]['content'], 'mensaje B')
        chat, reset_a, message, status = self.env['nueva_conversacion_web']()
        self.assertEqual((chat, reset_a, message, status), ([], [], '', ''))
        self.assertEqual(b[0]['content'], 'mensaje B')
        list(respond('otra pregunta', reset_a))
        self.assertEqual([m['role'] for m in self.tokenizer.messages], ['system', 'user'])

    def test_limits_prune_complete_exchanges_and_reject_long_input(self):
        generate = self.env['generar_respuesta_web']
        memory = []
        for i in range(5):
            _, memory = generate(f'mensaje {i}', memory)
        self.assertEqual(len(memory), 6)
        self.assertEqual(memory[0]['content'], 'mensaje 2')
        self.env['MAX_TOKENS_ENTRADA_WEB'] = len(self.env['PERSONALIDAD_WEB']) + len('hola')
        _, memory = generate('hola', memory)
        self.assertEqual([m['role'] for m in self.tokenizer.messages], ['system', 'user'])
        self.assertEqual(len(memory), 2)
        with self.assertRaises(ValueError):
            generate('demasiado largo', memory)

    def test_generation_errors_keep_history_and_allow_retry(self):
        respond = self.env['responder_web']
        memory = list(respond('hola', []))[-1][1]
        self.model.fail = True
        updates = list(respond('otra', memory))
        self.assertEqual(updates[0][-1], 'Blue está pensando…')
        self.assertEqual(updates[-1][1], memory)
        self.assertEqual(updates[-1][2]['value'], 'otra')
        self.assertTrue(updates[-1][2]['interactive'])
        self.assertNotIn('error interno', updates[-1][-1])
        self.assertEqual(list(respond(' ', memory))[-1][1], memory)

    def test_section_reuses_model_and_enables_public_link_explicitly(self):
        self.assertNotIn('from_pretrained', self.web_source + self.ui_source + self.launch_source)
        self.assertIn('share=True', self.launch_source)
        self.assertIn('concurrency_limit=1', self.ui_source)
