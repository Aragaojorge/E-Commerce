def validate_ssn(ssn):
    # Remover caracteres não numéricos
    ssn = ''.join(filter(str.isdigit, ssn))
    
    # Verificar se o CPF tem 11 dígitos
    if len(ssn) != 11:
        return False

    # Calcular o primeiro dígito verificador
    soma = sum(int(ssn[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    if resto == 10 or resto == 11:
        resto = 0
    if resto != int(ssn[9]):
        return False

    # Calcular o segundo dígito verificador
    soma = sum(int(ssn[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    if resto == 10 or resto == 11:
        resto = 0
    if resto != int(ssn[10]):
        return False

    return True