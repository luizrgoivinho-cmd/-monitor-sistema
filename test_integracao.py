import unittest
from unittest.mock import patch
from coleta import coletar_cpu
from funcoes import verificar_cpu
from monitor import executar_ciclo
from types import SimpleNamespace


class TestarIntegracao(unittest.TestCase):

    @staticmethod
    def criar_estados_alerta():
        return {
            "cpu": False,
            "memoria": False,
            "disco": False
        }

    @staticmethod
    def criar_recursos_simulados(memoria, disco):
        memoria_simulada = SimpleNamespace(percent=memoria)
        disco_simulado = SimpleNamespace(percent=disco)

        return memoria_simulada, disco_simulado

    def test_coleta_e_verificacao_cpu(self):
        with patch("coleta.psutil.cpu_percent", return_value=90.0) as mock_cpu:
            cpu = coletar_cpu()
            resultado = verificar_cpu(cpu, limite=80)

        self.assertEqual(resultado, "CPU elevada: 90.0%")
        mock_cpu.assert_called_once_with(interval=1)

    def test_integracao_ciclo_monitoramento(self):
        estados_alerta = self.criar_estados_alerta()

        memoria, disco = self.criar_recursos_simulados(90.0, 90.0)

        with patch("coleta.psutil.cpu_percent", return_value=90.0) as mock_cpu, \
            patch("coleta.psutil.virtual_memory", return_value=memoria) as mock_memoria, \
                        patch("coleta.psutil.disk_usage", return_value=disco) as mock_disco, \
            patch("monitor.registrar_alertas") as mock_registrar:
            executar_ciclo(
                limite_cpu=80,
                limite_memoria=80,
                limite_disco=80,
                estados_alerta=estados_alerta
            )

        mock_cpu.assert_called_once_with(interval=1)
        mock_memoria.assert_called_once_with()
        mock_disco.assert_called_once_with("/")
        mock_registrar.assert_called_once()

        self.assertTrue(estados_alerta["cpu"])
        self.assertTrue(estados_alerta["memoria"])
        self.assertTrue(estados_alerta["disco"])

        alertas_registrados = mock_registrar.call_args.args[0]
        self.assertEqual(len(alertas_registrados), 3)
        self.assertIn("CPU elevada: 90.0%", alertas_registrados)
        self.assertIn("Memória RAM elevada: 90.0%", alertas_registrados)
        self.assertIn("uso do disco elevado: 90.0%", alertas_registrados)

    def test_integracao_ciclo_normal(self):
        estados_alerta = self.criar_estados_alerta()

        memoria, disco = self.criar_recursos_simulados(30.0, 30.0)

        with patch("coleta.psutil.cpu_percent", return_value=30.0), \
             patch("coleta.psutil.virtual_memory", return_value=memoria), \
             patch("coleta.psutil.disk_usage", return_value=disco), \
             patch("monitor.registrar_alertas") as mock_registrar:

            executar_ciclo(
                limite_cpu=80,
                limite_memoria=80,
                limite_disco=80,
                estados_alerta=estados_alerta
            )

        mock_registrar.assert_not_called()

        self.assertFalse(estados_alerta["cpu"])
        self.assertFalse(estados_alerta["memoria"])
        self.assertFalse(estados_alerta["disco"])

    def test_integracao_alerta_somente_cpu(self):
        estados_alerta = self.criar_estados_alerta()

        memoria, disco = self.criar_recursos_simulados(30.0, 30.0)

        with patch("coleta.psutil.cpu_percent", return_value=90.0), \
             patch("coleta.psutil.virtual_memory", return_value=memoria), \
             patch("coleta.psutil.disk_usage", return_value=disco), \
             patch("monitor.registrar_alertas") as mock_registrar:

            executar_ciclo(
                limite_cpu=80,
                limite_memoria=80,
                limite_disco=80,
                estados_alerta=estados_alerta
            )

        mock_registrar.assert_called_once()

        alertas_registrados = mock_registrar.call_args.args[0]

        self.assertEqual(len(alertas_registrados), 1)
        self.assertIn("CPU elevada: 90.0%", alertas_registrados)

        self.assertTrue(estados_alerta["cpu"])
        self.assertFalse(estados_alerta["memoria"])
        self.assertFalse(estados_alerta["disco"])

    def test_integracao_alerta_somente_memoria(self):
        estados_alerta = self.criar_estados_alerta()

        memoria, disco = self.criar_recursos_simulados(90.0, 30.0)

        with patch("coleta.psutil.cpu_percent", return_value=30.0), \
             patch("coleta.psutil.virtual_memory", return_value=memoria), \
             patch("coleta.psutil.disk_usage", return_value=disco), \
             patch("monitor.registrar_alertas") as mock_registrar:

            executar_ciclo(
                limite_cpu=80,
                limite_memoria=80,
                limite_disco=80,
                estados_alerta=estados_alerta
            )

        mock_registrar.assert_called_once()

        alertas_registrados = mock_registrar.call_args.args[0]

        self.assertEqual(len(alertas_registrados), 1)
        self.assertIn("Memória RAM elevada: 90.0%", alertas_registrados)

        self.assertFalse(estados_alerta["cpu"])
        self.assertTrue(estados_alerta["memoria"])
        self.assertFalse(estados_alerta["disco"])

    def test_integracao_alerta_somente_disco(self):
        estados_alerta = self.criar_estados_alerta()

        memoria, disco = self.criar_recursos_simulados(30.0, 90.0)

        with patch("coleta.psutil.cpu_percent", return_value=30.0), \
             patch("coleta.psutil.virtual_memory", return_value=memoria), \
             patch("coleta.psutil.disk_usage", return_value=disco), \
             patch("monitor.registrar_alertas") as mock_registrar:

            executar_ciclo(
                limite_cpu=80,
                limite_memoria=80,
                limite_disco=80,
                estados_alerta=estados_alerta
            )

        mock_registrar.assert_called_once()

        alertas_registrados = mock_registrar.call_args.args[0]

        self.assertEqual(len(alertas_registrados), 1)
        self.assertIn("uso do disco elevado: 90.0%", alertas_registrados)

        self.assertFalse(estados_alerta["cpu"])
        self.assertFalse(estados_alerta["memoria"])
        self.assertTrue(estados_alerta["disco"])

    def test_integracao_normalizacao_cpu(self):
        estados_alerta = self.criar_estados_alerta()

        memoria, disco = self.criar_recursos_simulados(30.0, 30.0)

        with patch(
            "coleta.psutil.cpu_percent",
            side_effect=[90.0, 30.0]
        ) as mock_cpu, \
             patch(
                 "coleta.psutil.virtual_memory",
                 return_value=memoria
             ), \
             patch(
                 "coleta.psutil.disk_usage",
                 return_value=disco
             ), \
             patch("monitor.registrar_alertas") as mock_registrar:

            executar_ciclo(
                limite_cpu=80,
                limite_memoria=80,
                limite_disco=80,
                estados_alerta=estados_alerta
            )

            executar_ciclo(
                limite_cpu=80,
                limite_memoria=80,
                limite_disco=80,
                estados_alerta=estados_alerta
            )

        mock_cpu.assert_has_calls([
            unittest.mock.call(interval=1),
            unittest.mock.call(interval=1)
        ])

        self.assertEqual(mock_registrar.call_count, 2)

        alertas_primeiro_ciclo = (
            mock_registrar.call_args_list[0].args[0]
        )

        alertas_segundo_ciclo = (
            mock_registrar.call_args_list[1].args[0]
        )

        self.assertEqual(len(alertas_primeiro_ciclo), 1)
        self.assertIn(
            "CPU elevada: 90.0%",
            alertas_primeiro_ciclo
        )

        self.assertEqual(len(alertas_segundo_ciclo), 1)
        self.assertIn(
            "CPU normalizada: 30.0%",
            alertas_segundo_ciclo
        )

        self.assertFalse(estados_alerta["cpu"])
        self.assertFalse(estados_alerta["memoria"])
        self.assertFalse(estados_alerta["disco"])
