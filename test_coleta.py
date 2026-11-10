import unittest
from unittest.mock import patch
from coleta import coletar_cpu, coletar_memoria, coletar_disco

class TestarColeta(unittest.TestCase):

    def test_coletar_cpu(self):
        with patch("coleta.psutil.cpu_percent") as mock_cpu:
            mock_cpu.return_value = 25.5

            resultado = coletar_cpu()

            self.assertEqual(resultado, 25.5)
            mock_cpu.assert_called_once_with(interval=1)

    def test_coletar_memoria(self):
        memoria_simulada = "memoria de teste"

        with patch("coleta.psutil.virtual_memory") as mock_memoria:
            mock_memoria.return_value = memoria_simulada

            resultado = coletar_memoria()

            self.assertEqual(resultado, memoria_simulada)
            mock_memoria.assert_called_once_with()

    def test_coletar_disco(self):
        disco_simulado = "disco de teste"

        with patch("coleta.psutil.disk_usage") as mock_disco:
            mock_disco.return_value = disco_simulado

            resultado = coletar_disco()

            self.assertEqual(resultado, disco_simulado)
            mock_disco.assert_called_once_with("/")

if __name__ == "__main__":
    unittest.main()
