# -*- coding: utf-8 -*-
from teste.test_sce import TestSce
from datetime import datetime


class CasoTeste(TestSce):
    def test_inclui_socio_empresa(self):
        '''
        Teste para incluir sócio da empresa
        :param inicio:
        :return:
        '''
        # Cadastra empresa
        self.cadastra_empresa(empresa='empresa')


def main():
    teste = CasoTeste(banco='sce', background=True)
    teste.test_inclui_socio_empresa()


if __name__ == '__main__':
    main()
