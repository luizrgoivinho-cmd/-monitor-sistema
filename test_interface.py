import unittest
from unittest.mock import patch

from interface import (
    limpar_tela,
    exibir_cabecalho,
    exibir_recursos,
    exibir_status,
    exibir_rodape
)

class TestarInterface(unittest.TestCase):

    @patch("interface.os.system")
    def test_limpar_tela(self, mock_system):
        limpar_tela()

        mock_system.assert_called_once_with("clear")

    def test_exibir_cabecalho(self):
        with patch("builtins.print") as mock_print:
            exibir_cabecalho()

            chamadas = [
                call.args[0] for call in mock_print.call_args_list
            ]

            self.assertEqual(chamadas, [
                "=" * 35,
                "       MONITOR DE SISTEMAS",
                "=" * 35
            ])


    def test_exibir_recursos(self):
        with patch("builtins.print") as mock_print:
            exibir_recursos(25.5, 70.0, 80.0)

            chamadas = [
                call.args[0] for call in mock_print.call_args_list
            ]

            self.assertEqual(chamadas, [
                "\nCPU:       25.5%",
                "Memória:   70.0%",
                "Disco:     80.0%"
            ])

    def test_exibir_status_alerta(self):
        with patch("builtins.print") as mock_print:
            exibir_status(["CPU elevada: 90%"])

            mock_print.assert_called_once_with(
                "\nStatus: Alerta! Uso elevado."
            )

    def test_exibir_status_normal(self):
        with patch("builtins.print") as mock_print:
            exibir_status([])

            mock_print.assert_called_once_with(
                "\nStatus: Sistema normal."
            )

    def test_exibir_rodape(self):
        with patch("builtins.print") as mock_print:
            exibir_rodape()

            chamadas = [
                call.args[0] for call in mock_print.call_args_list
            ]

            self.assertEqual(chamadas, [
                "=" * 35,
                "\nAtualizando a cada 2 segundos...",
                "=" * 35
            ])

if __name__ == "__main__":
    unittest.main()