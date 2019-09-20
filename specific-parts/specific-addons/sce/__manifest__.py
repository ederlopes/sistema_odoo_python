# -*- coding: utf-8 -*-
{
    'name': "e-SCE",

    'summary': """
        e-SCE
        """,
    'description': """
        e-SCE
    """,
    'author': "ABGF",
    'website': "http://www.abgf.gov.br",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'website', 'inputmask_widget', 'base_search_fuzzy',
                'web_widget_x2many_2d_matrix',
                'cotacao_moeda'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/adicionar_funcionario_wizard.xml',
        'wizard/parecer_tecnico_exportador_wizard.xml',
        'data/auth_signup_data.xml',
        'data/website_data.xml',
        'data/ir_mail_server_data.xml',
        'data/res_config_settings_execute.xml',
        'data/linha_negocio_data.xml',
        'data/modalidade_data.xml',
        'data/natureza_juridica_data.xml',
        'data/natureza_risco_data.xml',
        'data/validacao_data.xml',
        'data/setor_atividade_data.xml',
        'data/res_bank_data.xml',
        'data/instituicao_financeira_data.xml',
        'data/gecex_data.xml',
        'data/agencia_data.xml',
        'data/email_notificacao_recusado_exportador.xml',
        'data/email_notificacao_exportador_enviado_analise.xml',
        'data/email_notificacao_aprovar_exportador.xml',
        'data/email_notificacao_envio_operacao_analista.xml',
        'data/tipo_financiamento_data.xml',
        'data/status_data.xml',
        'views/auth_signup.xml',
        'views/res_partner_user.xml',
        'views/res_partner_importador.xml',
        'views/res_partner_exportador.xml',
        'views/funcionario_exportador.xml',
        'views/portal_templates.xml',
        'views/verificar_email.xml',
        'views/linha_negocio.xml',
        'views/modalidade.xml',
        'views/valores_paises.xml',
        'views/socio.xml',
        'views/natureza_juridica.xml',
        'views/natureza_risco.xml',
        'views/res_bank.xml',
        'views/res_user.xml',
        'views/validacao.xml',
        'views/template_arquivos.xml',
        'views/instituicao_financeira.xml',
        'views/fundo.xml',
        'views/menu.xml',
    ],
    'qweb': [
        'static/src/xml/template.xml'
    ],
    'application': True,
    'bootstrap': True,
    'post_init_hook': 'post_init_hook',
}
