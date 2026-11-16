import unittest
from unittest.mock import patch, call

import monitor

def criar_recurso_simulado(percent):
    return type(
        "Recurso",
        (),
        {"percent": percent}
    )()

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
        memoria_simulada = criar_recurso_simulado(50.0)
        disco_simulado = criar_recurso_simulado(60.0)

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

        memoria_simulada = criar_recurso_simulado(50.0)
        disco_simulado = criar_recurso_simulado(60.0)

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

        memoria_simulada = criar_recurso_simulado(50.0)
        disco_simulado = criar_recurso_simulado(60.0)

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

        memoria_simulada = criar_recurso_simulado(50.0)
        disco_simulado = criar_recurso_simulado(60.0)

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
            criar_recurso_simulado(90.0),
            criar_recurso_simulado(95.0)
        ]

        discos_simulados = [
            criar_recurso_simulado(90.0),
            criar_recurso_simulado(95.0)
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
            criar_recurso_simulado(90.0),
            criar_recurso_simulado(50.0)
        ]

        discos_simulados = [
            criar_recurso_simulado(90.0),
            criar_recurso_simulado(60.0)
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


    def test_executar_ciclo_coletar_recursos(self):
        memoria_simulada = criar_recurso_simulado(50.0)
        disco_simulado = criar_recurso_simulado(60.0)

        estados_alerta = {
            "cpu": False,
            "memoria": False,
            "disco": False
        }

        with patch("monitor.coletar_cpu", return_value=30.0) as mock_cpu:
            with patch("monitor.coletar_memoria", return_value=memoria_simulada) as mock_memoria:
                with patch("monitor.coletar_disco", return_value=disco_simulado) as mock_disco:

                    with patch("monitor.limpar_tela"):
                        with patch("monitor.exibir_cabecalho"):
                            with patch("monitor.exibir_recursos") as mock_recursos:
                                with patch("monitor.exibir_status"):
                                    with patch("monitor.exibir_rodape"):

                                        monitor.executar_ciclo(
                                            80,
                                            80,
                                            80,
                                            estados_alerta
                                        )

        mock_cpu.assert_called_once()
        mock_memoria.assert_called_once()
        mock_disco.assert_called_once()

        mock_recursos.assert_called_once_with(
            30.0,
            50.0,
            60.0
        )

    def test_executar_ciclo_alerta_cpu(self):
        memoria_simulada = criar_recurso_simulado(50.0)
        disco_simulado = criar_recurso_simulado(60.0)

        estados_alerta = {
            "cpu": False,
            "memoria": False,
            "disco": False
        }

        with patch("monitor.coletar_cpu", return_value=90.0) as mock_cpu:
            with patch("monitor.coletar_memoria", return_value=memoria_simulada) as mock_memoria:
                with patch("monitor.coletar_disco", return_value=disco_simulado) as mock_disco:

                    with patch("monitor.limpar_tela"):
                        with patch("monitor.exibir_cabecalho"):
                            with patch("monitor.exibir_recursos") as mock_recursos:
                                with patch("monitor.exibir_status"):
                                    with patch("monitor.registrar_alertas") as mock_registrar:
                                        with patch("monitor.exibir_rodape"):

                                            monitor.executar_ciclo(
                                                80,
                                                80,
                                                80,
                                                estados_alerta
                                            )

        mock_cpu.assert_called_once()
        mock_memoria.assert_called_once()
        mock_disco.assert_called_once()

        mock_recursos.assert_called_once_with(
            90.0,
            50.0,
            60.0
        )

        self.assertTrue(estados_alerta["cpu"])

        mock_registrar.assert_called_once_with([
            "CPU elevada: 90.0%"
        ])

    def test_executar_ciclo_normalizar_cpu(self):
        memoria_simulada = criar_recurso_simulado(50.0)
        disco_simulado = criar_recurso_simulado(60.0)

        estados_alerta = {
            "cpu": False,
            "memoria": False,
            "disco": False
        }

        with patch("monitor.coletar_cpu", side_effect=[90.0, 30.0]) as mock_cpu:
            with patch("monitor.coletar_memoria", return_value=memoria_simulada) as mock_memoria:
                with patch("monitor.coletar_disco", return_value=disco_simulado) as mock_disco:

                    with patch("monitor.limpar_tela"):
                        with patch("monitor.exibir_cabecalho"):
                            with patch("monitor.exibir_recursos") as mock_recursos:
                                with patch("monitor.exibir_status"):
                                    with patch("monitor.registrar_alertas") as mock_registrar:
                                        with patch("monitor.exibir_rodape"):

                                            monitor.executar_ciclo(
                                                80,
                                                80,
                                                80,
                                                estados_alerta
                                            )

                                            monitor.executar_ciclo(
                                                80,
                                                80,
                                                80,
                                                estados_alerta
                                            )

        mock_cpu.assert_has_calls([
            call(),
            call()
        ])

        self.assertEqual(mock_cpu.call_count, 2)

        self.assertEqual(mock_memoria.call_count, 2)
        self.assertEqual(mock_disco.call_count, 2)

        mock_recursos.assert_has_calls([
            call(90.0, 50.0, 60.0),
            call(30.0, 50.0, 60.0)
        ])

        self.assertEqual(mock_recursos.call_count, 2)
        self.assertFalse(estados_alerta["cpu"])


        mock_registrar.assert_has_calls([
            call(["CPU elevada: 90.0%"]),
            call(["CPU normalizada: 30.0%"])
        ])

        self.assertEqual(mock_registrar.call_count, 2)

    def test_executar_ciclo_alerta_memoria(self):
        memoria_simulada = criar_recurso_simulado(90.0)
        disco_simulado = criar_recurso_simulado(60.0)

        estados_alerta = {
            "cpu": False,
            "memoria": False,
            "disco": False
        }

        with patch("monitor.coletar_cpu", return_value=30.0) as mock_cpu:
            with patch("monitor.coletar_memoria", return_value=memoria_simulada) as mock_memoria:
                with patch("monitor.coletar_disco", return_value=disco_simulado) as mock_disco:

                    with patch("monitor.limpar_tela"):
                        with patch("monitor.exibir_cabecalho"):
                            with patch("monitor.exibir_recursos") as mock_recursos:
                                with patch("monitor.exibir_status"):
                                    with patch("monitor.registrar_alertas") as mock_registrar:
                                        with patch("monitor.exibir_rodape"):

                                            monitor.executar_ciclo(
                                                80,
                                                80,
                                                80,
                                                estados_alerta
                                            )

        mock_cpu.assert_called_once()
        mock_memoria.assert_called_once()
        mock_disco.assert_called_once()

        mock_recursos.assert_called_once_with(
            30.0,
            90.0,
            60.0
        )

        self.assertTrue(estados_alerta["memoria"])


        mock_registrar.assert_called_once_with([
            "Memória RAM elevada: 90.0%"
        ])

    def test_executar_ciclo_normalizar_memoria(self):

        memoria_simulada_1 = criar_recurso_simulado(90.0)
        memoria_simulada_2 = criar_recurso_simulado(50.0)
        disco_simulado = criar_recurso_simulado(60.0)

        estados_alerta = {
            "cpu": False,
            "memoria": False,
            "disco": False
        }

        with patch("monitor.coletar_cpu", return_value=30.0) as mock_cpu:
            with patch(
                "monitor.coletar_memoria",
                side_effect=[memoria_simulada_1, memoria_simulada_2]
            ) as mock_memoria:
                with patch("monitor.coletar_disco", return_value=disco_simulado) as mock_disco:
                    with patch("monitor.limpar_tela"):
                        with patch("monitor.exibir_cabecalho"):
                            with patch("monitor.exibir_recursos") as mock_recursos:
                                with patch("monitor.exibir_status"):
                                    with patch("monitor.registrar_alertas") as mock_registrar:
                                        with patch("monitor.exibir_rodape"):

                                            monitor.executar_ciclo(
                                                80,
                                                80,
                                                80,
                                                estados_alerta
                                            )

                                            monitor.executar_ciclo(
                                                80,
                                                80,
                                                80,
                                                estados_alerta
                                            )

        mock_cpu.assert_has_calls([
            call(),
            call()
        ])

        self.assertEqual(mock_cpu.call_count, 2)

        self.assertEqual(mock_memoria.call_count, 2)
        self.assertEqual(mock_disco.call_count, 2)

        mock_recursos.assert_has_calls([
            call(30.0, 90.0, 60.0),
            call(30.0, 50.0, 60.0)
        ])

        self.assertEqual(mock_recursos.call_count, 2)
        self.assertFalse(estados_alerta["memoria"])


        mock_registrar.assert_has_calls([
            call(["Memória RAM elevada: 90.0%"]),
            call(["Memória RAM normalizada: 50.0%"])
        ])

        self.assertEqual(mock_registrar.call_count, 2)

    def test_executar_ciclo_alerta_disco(self):
        memoria_simulada = criar_recurso_simulado(50.0)
        disco_simulado = criar_recurso_simulado(90.0)

        estados_alerta = {
            "cpu": False,
            "memoria": False,
            "disco": False
        }

        with patch("monitor.coletar_cpu", return_value=30.0) as mock_cpu:
            with patch("monitor.coletar_memoria", return_value=memoria_simulada) as mock_memoria:
                with patch("monitor.coletar_disco", return_value=disco_simulado) as mock_disco:

                    with patch("monitor.limpar_tela"):
                        with patch("monitor.exibir_cabecalho"):
                            with patch("monitor.exibir_recursos") as mock_recursos:
                                with patch("monitor.exibir_status"):
                                    with patch("monitor.registrar_alertas") as mock_registrar:
                                        with patch("monitor.exibir_rodape"):

                                            monitor.executar_ciclo(
                                                80,
                                                80,
                                                80,
                                                estados_alerta
                                            )

        mock_cpu.assert_called_once()
        mock_memoria.assert_called_once()
        mock_disco.assert_called_once()

        mock_recursos.assert_called_once_with(
            30.0,
            50.0,
            90.0
        )

        self.assertTrue(estados_alerta["disco"])


        mock_registrar.assert_called_once_with([
            "uso do disco elevado: 90.0%"
        ])

    def test_executar_ciclo_normalizar_disco(self):

        memoria_simulada = criar_recurso_simulado(50.0)

        disco_simulado_1 = criar_recurso_simulado(90.0)
        disco_simulado_2 = criar_recurso_simulado(60.0)

        estados_alerta = {
            "cpu": False,
            "memoria": False,
            "disco": False
        }

        with patch("monitor.coletar_cpu", return_value=30.0) as mock_cpu:
            with patch(
                    "monitor.coletar_memoria",
                    return_value=memoria_simulada
                ) as mock_memoria:
                with patch(
                        "monitor.coletar_disco",
                        side_effect=[disco_simulado_1, disco_simulado_2]
                    ) as mock_disco:
                    with patch("monitor.limpar_tela"):
                        with patch("monitor.exibir_cabecalho"):
                            with patch("monitor.exibir_recursos") as mock_recursos:
                                with patch("monitor.exibir_status"):
                                    with patch("monitor.registrar_alertas") as mock_registrar:
                                        with patch("monitor.exibir_rodape"):

                                            monitor.executar_ciclo(
                                                80,
                                                80,
                                                80,
                                                estados_alerta
                                            )

                                            monitor.executar_ciclo(
                                                80,
                                                80,
                                                80,
                                                estados_alerta
                                            )

        mock_cpu.assert_has_calls([
            call(),
            call()
        ])

        self.assertEqual(mock_cpu.call_count, 2)

        self.assertEqual(mock_memoria.call_count, 2)
        self.assertEqual(mock_disco.call_count, 2)

        mock_recursos.assert_has_calls([
            call(30.0, 50.0, 90.0),
            call(30.0, 50.0, 60.0)
        ])

        self.assertEqual(mock_recursos.call_count, 2)
        self.assertFalse(estados_alerta["disco"])


        mock_registrar.assert_has_calls([
            call(["uso do disco elevado: 90.0%"]),
            call(["Disco normalizado: 60.0%"])
        ])

        self.assertEqual(mock_registrar.call_count, 2)


if __name__ == "__main__":
    unittest.main()