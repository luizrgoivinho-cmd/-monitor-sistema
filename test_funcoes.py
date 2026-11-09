import unittest
from funcoes import obter_limite
from unittest.mock import patch, mock_open
from funcoes import escolher_limite
from funcoes import verificar_cpu
from funcoes import verificar_memoria
from funcoes import verificar_disco
from funcoes import normalizar_cpu
from funcoes import registrar_alertas
from funcoes import controlar_alerta


class TestarObterLimite(unittest.TestCase):

    @patch("builtins.input", return_value="80")
    def test_limite_valido(self, entrada_simulada):
        self.assertEqual(obter_limite("CPU"), 80.0)

    @patch("builtins.input", side_effect=["150", "80"])
    def test_limite_acima_do_permitido(self, entrada_simulada):
        resultado = obter_limite("CPU")

        self.assertEqual(resultado, 80.0)
        self.assertEqual(entrada_simulada.call_count, 2)

    @patch("builtins.input", side_effect=["abc", "80"])
    def test_entrada_nao_numerica(self, entrada_simulada):
        resultado = obter_limite("CPU")

        self.assertEqual(resultado, 80.0)
        self.assertEqual(entrada_simulada.call_count, 2)

    @patch("builtins.input", side_effect=["-10", "50"])
    def test_limite_negativo(self, entrada_simulada):
        resultado = obter_limite("CPU")

        self.assertEqual(resultado, 50.0)
        self.assertEqual(entrada_simulada.call_count, 2)

    @patch("builtins.input", return_value="0")
    def test_limite_zero(self, entrada_simulada):
        resultado = obter_limite("CPU")

        self.assertEqual(resultado, 0.0)
        self.assertEqual(entrada_simulada.call_count, 1)

    @patch("builtins.input", return_value="n")
    def test_escolher_limite_padrao(self, entrada_simulada):
        resultado = escolher_limite("CPU")

        self.assertEqual(resultado, 80)

    @patch("funcoes.obter_limite", return_value=65)
    @patch("builtins.input", return_value="s")
    def test_escolher_limite_personalizado(
        self, entrada_simulada, limite_simulado
    ):
        resultado = escolher_limite("CPU")

        self.assertEqual(resultado, 65)
        limite_simulado.assert_called_once_with("CPU")

    @patch("builtins.input", side_effect=["talvez", "n"])
    def test_resposta_invalida(self, entrada_simulada):
        resultado = escolher_limite("CPU")

        self.assertEqual(resultado, 80)
        self.assertEqual(entrada_simulada.call_count, 2)

    @patch("builtins.print")
    def test_registrar_alertas(self, print_simulado):
        arquivo_simulado = mock_open()

        with patch("builtins.open", arquivo_simulado):
            alertas = ["CPU elevada: 90%"]

            registrar_alertas(alertas)

        arquivo_simulado.assert_called_once_with("alerta.log", "a")

        arquivo_simulado().write.assert_called_once()

        mensagem_gravada = arquivo_simulado().write.call_args[0][0]

        self.assertIn("CPU elevada: 90%", mensagem_gravada)
        print_simulado.assert_called_once()

    def test_cpu_elevada(self):
        resultado = verificar_cpu(90, 80)

        self.assertEqual(resultado, "CPU elevada: 90%")

    def test_cpu_normal(self):
        resultado = verificar_cpu(50, 80)

        self.assertIsNone(resultado)

    def test_memoria_elevada(self):
        resultado = verificar_memoria(90, 80)

        self.assertEqual(resultado, "Memória RAM elevada: 90%")

    def test_memoria_normal(self):
        resultado = verificar_memoria(60, 80)

        self.assertIsNone(resultado)

    def test_disco_elevado(self):
        resultado = verificar_disco(90, 80)

        self.assertEqual(resultado, "uso do disco elevado: 90%")

    def test_disco_normal(self):
        resultado = verificar_disco(60, 80)

        self.assertIsNone(resultado)

    def test_normalizar_cpu(self):
        resultado = normalizar_cpu(50)

        self.assertEqual(resultado, "CPU normalizada: 50%")

    def test_novo_alerta(self):
        resultado = controlar_alerta(False, "CPU elevada: 90%", "CPU normalizada: 50%")

        self.assertEqual(resultado, (["CPU elevada: 90%"], True))

    def test_alerta_repetindo(self):
        resultado = controlar_alerta(True, "CPU elevada: 95%", "CPU normalizada: 50%")

        self.assertEqual(resultado, ([], True))

    def test_normalizacao(self):
        resultado = controlar_alerta(
            True,
            None,
            "CPU normalizada: 50%"
        )

        self.assertEqual(
            resultado,
            (["CPU normalizada: 50%"], False)
        )

    def test_normalizacao_repetida(self):
        resultado = controlar_alerta(
            False,
            None,
            "CPU normalizada: 45%"
        )

        self.assertEqual(resultado, ([], False))

if __name__ == "__main__":
    unittest.main()
