"""Pruebas sin red ni modelo: formato y comportamiento del historial."""
import ast
from contextlib import nullcontext
import json
from pathlib import Path
import unittest

NOTEBOOK = Path(__file__).resolve().parents[1] / "Blue_IA_Experimento_001.ipynb"


class FakeTokens:
    def __init__(self, length):
        self.shape = (1, length)

    def to(self, device):
        return self


class FakeTokenizer:
    eos_token_id = 0

    def apply_chat_template(self, messages, **kwargs):
        self.messages = messages
        return FakeTokens(sum(len(m["content"]) for m in messages))

    def decode(self, tokens, **kwargs):
        return "respuesta de prueba"


class FakeOutput:
    def __getitem__(self, item):
        return []


class FakeModel:
    fail = False

    def generate(self, **kwargs):
        if self.fail:
            raise RuntimeError("fallo de generación")
        return FakeOutput()


class FakeTorch:
    @staticmethod
    def inference_mode():
        return nullcontext()

    @staticmethod
    def ones_like(tokens):
        return tokens


class NotebookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
        cls.sources = ["".join(cell["source"]) for cell in cls.notebook["cells"]]
        cls.blue_source = next(s for s in cls.sources if "def hablar_con_blue(" in s)

    def setUp(self):
        self.tokenizer = FakeTokenizer()
        self.model = FakeModel()
        self.env = {"tokenizador": self.tokenizer, "modelo": self.model,
                    "torch": FakeTorch(), "dispositivo": "cpu"}
        exec(compile(self.blue_source, "blue_cell", "exec"), self.env)

    def test_notebook_format_and_python_syntax(self):
        self.assertEqual(self.notebook["nbformat"], 4)
        self.assertEqual(len({c["id"] for c in self.notebook["cells"]}), len(self.notebook["cells"]))
        for cell in self.notebook["cells"]:
            if cell["cell_type"] == "code":
                ast.parse("".join(cell["source"]))
                self.assertEqual(cell["outputs"], [])

    def test_history_is_limited_and_reset(self):
        for i in range(5):
            self.env["hablar_con_blue"](f"pregunta {i}")
        history = self.env["historial"]
        self.assertEqual(len(history), 6)
        self.assertEqual(history[0]["content"], "pregunta 2")
        self.env["reiniciar_conversacion"]()
        self.assertEqual(history, [])

    def test_long_input_prunes_pairs_and_rejects_oversize(self):
        self.env["hablar_con_blue"]("primera")
        self.env["hablar_con_blue"]("segunda")
        base = len(self.env["INSTRUCCIONES_BLUE"])
        self.env["MAX_TOKENS_ENTRADA"] = base + len("actual")
        self.env["hablar_con_blue"]("actual")
        self.assertEqual(len(self.env["historial"]), 2)
        previous = self.env["historial"][:]
        with self.assertRaises(ValueError):
            self.env["hablar_con_blue"]("x" * 1000)
        self.assertEqual(self.env["historial"], previous)

    def test_invalid_input_and_generation_error_do_not_change_history(self):
        self.env["hablar_con_blue"]("hola")
        previous = self.env["historial"][:]
        for message in (" ", None):
            with self.assertRaises(ValueError):
                self.env["hablar_con_blue"](message)
        self.model.fail = True
        with self.assertRaises(RuntimeError):
            self.env["hablar_con_blue"]("otra")
        self.assertEqual(self.env["historial"], previous)


if __name__ == "__main__":
    unittest.main()
