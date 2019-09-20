$(document).ready(function(){

    $(".porcentagem").inputmask({mask: '99.99'});

    $("body").on('change', "select[name=tipo_socio]", function(){

        $("input[name=cpf_cnpj]").inputmask('remove');
        if ( $(this).val() == "\"PF\"")
        {
            $("input[name=cpf_cnpj]").inputmask({mask: '999.999.999-99'});
            $(".label_cpf_cnpj").html('CPF');
        }else{
            $("input[name=cpf_cnpj]").inputmask({mask: '99.999.999/9999-99'});
            $(".label_cpf_cnpj").html('CNPJ');
        }
    })

})
