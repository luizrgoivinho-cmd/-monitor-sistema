import unittest
from unittest.mock import patch, call

import monitor

class TestarMonitor(unittest.TestCase):

    def test_configurar_limites(self):
        with patch(
            "monitor.escolher_limite",
            return_value=80
        ) as mock_escolher:

            with patch(
                "monitor.coletar_cpu",
                side_effect=StopIteration
            ):
                with self.assertRaises(StopIteration):
                    monitor.main()

        mock_escolher.assert_has_calls([
            call("CPU"),
            call("memória"),
            call("disco")
        ])

        self.assertEqual(mock_escolher.call_count, 3)


    def test_coletar_recursos(self):
        memoria_simulada = type(
            "Memoria",
            (),
            {"percent": 50.0}
        )()

        disco_simulado = type(
            "Disco",
            (),
            {"percent": 60.0}
        )()

        with patch("monitor.escolher_limite", return_value=80):
            with patch("monitor.coletar_cpu", return_value=30.0) as mock_cpu:
                with patch("monitor.coletar_memoria", return_value=memoria_simulada) as mock_memoria:
                    with patch("monitor.coletar_disco", return_value=disco_simulado) as mock_disco:

                        with patch("monitor.limpar_tela"):
                            with patch("monitor.exibir_cabecalho"):
                                with patch("monitor.exibir_recursos"):
                                    with patch("monitor.exibir_status"):
                                        with patch("monitor.exibir_rodape"):
                                            with patch("monitor.time.sleep", side_effect=StopIteration):
                                                with self.assertRaises(StopIteration):
                                                    monitor.main()
        mock_cpu.assert_called_once()
        mock_memoria.assert_called_once()
        mock_disco.assert_called_once()

    def test_identificar_alerta_cpu(self):
        memoria_simulada = type(
            "Memoria",
            (),
            {"percent": 50.0}
        )()

        disco_simulado = type(
            "Disco",
            (),
            {"percent": 60.0}
        )()

        with patch("monitor.escolher_limite", return_value=80):
            with patch("monitor.coletar_cpu", return_value=90.0):
                with patch("monitor.coletar_memoria", return_value=memoria_simulada):
                    with patch("monitor.coletar_disco", return_value=disco_simulado):

                        with patch("monitor.limpar_tela"):
                            with patch("monitor.exibir_cabecalho"):
                                with patch("monitor.exibir_recursos"):
                                    with patch("monitor.exibir_status"):
                                        with patch("monitor.exibir_rodape"):
                                            with patch("monitor.registrar_alertas") as mock_registrar:
                                                with patch("monitor.time.sleep", side_effect=StopIteration):
                                                    with self.assertRaises(StopIteration):
                                                        monitor.main()

        mock_registrar.assert_called_once_with([
            "CPU elevada: 90.0%"
        ])

    def test_normalizar_cpu(self):
        memoria_simulada = type(
            "Memoria",
            (),
            {"percent": 50.0}
        )()

        disco_simulado = type(
            "Disco",
            (),
            {"percent": 60.0}
        )()

        with patch("monitor.escolher_limite", return_value=80):
            with patch("monitor.coletar_cpu", side_effect=[90.0, 30.0]):
                with patch("monitor.coletar_memoria", return_value=memoria_simulada):
                    with patch("monitor.coletar_disco", return_value=disco_simulado):

                        with patch("monitor.limpar_tela"):
                            with patch("monitor.exibir_cabecalho"):
                                with patch("monitor.exibir_recursos"):
                                    with patch("monitor.exibir_status"):
                                        with patch("monitor.exibir_rodape"):
                                            with patch("monitor.registrar_alertas") as mock_registrar:
                                                with patch("monitor.time.sleep", side_effect=[None, StopIteration]):
                                                    with self.assertRaises(StopIteration):
                                                        monitor.main()

        mock_registrar.assert_has_calls([
            call(["CPU elevada: 90.0%"]),
            call(["CPU normalizada: 30.0%"])
        ])

        self.assertEqual(mock_registrar.call_count, 2)

    def test_evitar_alertas_repetidos(self):
        memoria_simulada = type(
            "Memoria",
            (),
            {"percent": 50.0}
        )()

        disco_simulado = type(
            "Disco",
            (),
            {"percent": 60.0}
        )()

        with patch("monitor.escolher_limite", return_value=80):
            with patch("monitor.coletar_cpu", side_effect=[90.0, 95.0]):
                with patch("monitor.coletar_memoria", return_value=memoria_simulada):
                    with patch("monitor.coletar_disco", return_value=disco_simulado):

                        with patch("monitor.limpar_tela"):
                            with patch("monitor.exibir_cabecalho"):
                                with patch("monitor.exibir_recursos"):
                                    with patch("monitor.exibir_status"):
                                        with patch("monitor.exibir_rodape"):
                                            with patch("monitor.registrar_alertas") as mock_registrar:
                                                with patch("monitor.time.sleep", side_effect=[None, StopIteration]):
                                                    with self.assertRaises(StopIteration):
                                                        monitor.main()

        mock_registrar.assert_called_once_with([
            "CPU elevada: 90.0%"
        ])

    def test_evitar_alertas_repetidos_memoria_disco(self):
        memorias_simuladas = [
            type("Memoria", (), {"percent": 90.0})(),
            type("Memoria", (), {"percent": 95.0})()
        ]

        discos_simulados = [
            type("Disco", (), {"percent": 90.0})(),
            type("Disco", (), {"percent": 95.0})()
        ]

        with patch("monitor.escolher_limite", return_value=80):
            with patch("monitor.coletar_cpu", return_value=30.0):
                with patch("monitor.coletar_memoria", side_effect=memorias_simuladas):
                    with patch("monitor.coletar_disco", side_effect=discos_simulados):

                        with patch("monitor.limpar_tela"):
                            with patch("monitor.exibir_cabecalho"):
                                with patch("monitor.exibir_recursos"):
                                    with patch("monitor.exibir_status"):
                                        with patch("monitor.exibir_rodape"):
                                            with patch("monitor.registrar_alertas") as mock_registrar:
                                                with patch("monitor.time.sleep", side_effect=[None, StopIteration]):
                                                    with self.assertRaises(StopIteration):
                                                        monitor.main()

        mock_registrar.assert_called_once_with([
            "Memória RAM elevada: 90.0%",
            "uso do disco elevado: 90.0%"
        ])


    def test_normalizar_memoria_disco(self):
        memorias_simuladas = [
            type("Memoria", (), {"percent": 90.0})(),
            type("Memoria", (), {"percent": 50.0})()
        ]

        discos_simulados = [
            type("Disco", (), {"percent": 90.0})(),
            type("Disco", (), {"percent": 60.0})()
        ]

        with patch("monitor.escolher_limite", return_value=80):
            with patch("monitor.coletar_cpu", return_value=30.0):
                with patch("monitor.coletar_memoria", side_effect=memorias_simuladas):
                    with patch("monitor.coletar_disco", side_effect=discos_simulados):

                        with patch("monitor.limpar_tela"):
                            with patch("monitor.exibir_cabecalho"):
                                with patch("monitor.exibir_recursos"):
                                    with patch("monitor.exibir_status"):
                                        with patch("monitor.exibir_rodape"):
                                            with patch("monitor.registrar_alertas") as mock_registrar:
                                                with patch("monitor.time.sleep", side_effect=[None, StopIteration]):
                                                    with self.assertRaises(StopIteration):
                                                        monitor.main()

        mock_registrar.assert_has_calls([
            call([
                "Memória RAM elevada: 90.0%",
                "uso do disco elevado: 90.0%"
            ]),
            call([
                "Memória RAM normalizada: 50.0%",
                "Disco normalizado: 60.0%"
            ])
        ])

        self.assertEqual(mock_registrar.call_count, 2)


if __name__ == "__main__":
    unittest.main()