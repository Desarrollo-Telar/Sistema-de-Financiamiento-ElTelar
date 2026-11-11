from pathlib import Path
p=Path('pagare.py')
s=p.read_text(encoding='utf-8')
s=s.replace('    return datos\n', '''    # Una lista explícita sustituye los campos históricos de avalista único.
    entrada = datos_entrada or {}
    if "avalistas" in entrada:
        avalistas = entrada["avalistas"] or []
        if not isinstance(avalistas, (list, tuple)) or any(
            not isinstance(avalista, dict) for avalista in avalistas
        ):
            raise ValueError("avalistas debe ser una lista de diccionarios")
        datos["avalistas"] = [dict(avalista) for avalista in avalistas]
        datos["incluir_aval"] = bool(avalistas) and entrada.get("incluir_aval", True)
    elif datos.get("incluir_aval") or any(
        datos.get(campo) for campo in ("avalista_nombre", "avalista_dpi", "avalista_domicilio")
    ):
        datos["avalistas"] = [{
            "nombre": datos.get("avalista_nombre", ""),
            "dpi": datos.get("avalista_dpi", ""),
            "domicilio": datos.get("avalista_domicilio", ""),
        }]
        datos["incluir_aval"] = entrada.get("incluir_aval", True)
    else:
        datos["avalistas"] = []

    if datos["incluir_aval"]:
        firmantes = [(datos.get("deudor_nombre", ""), datos.get("deudor_dpi", ""))]
        firmantes.extend((aval.get("nombre", ""), aval.get("dpi", "")) for aval in datos["avalistas"])
        if "notario_firmantes" not in entrada:
            datos["notario_firmantes"] = "; ".join(nombre or "________________" for nombre, _ in firmantes)
        if "notario_cui_firmantes" not in entrada:
            datos["notario_cui_firmantes"] = [
                cui_dpi_a_letras(dpi)[0] if dpi else "________________" for _, dpi in firmantes
            ]

    return datos
''',1)
s=s.replace('    if datos.get("incluir_aval", True):\n', '    for indice, avalista in enumerate(datos["avalistas"] if datos["incluir_aval"] else [], start=1):\n',1)
s=s.replace('p_aval_tit.add_run("AVAL:")', 'p_aval_tit.add_run(f"AVAL {indice}:" if len(datos["avalistas"]) > 1 else "AVAL:")')
for field in ('nombre','dpi','domicilio'):
 s=s.replace("datos.get('avalista_"+field+"')", "avalista.get('"+field+"')")
a=s.index('        if len(firmantes_cui) >= 2:')
b=s.index('\n        p_autentica =',a)
s=s[:a]+'''        if len(firmantes_cui) > 1:
            cui_texto = "; ".join(f"firmante {i}: {cui}" for i, cui in enumerate(firmantes_cui, 1))
        elif firmantes_cui:
            cui_texto = firmantes_cui[0]
        else:
            cui_texto = "________________"
'''+s[b:]
s=s.replace('; ambos extendidos por el Registro', '; extendidos por el Registro')
a=s.index('    # Buscar si tiene garantía')
b=s.index('\n    datos = {',a)
s=s[:a]+'''    # Recorrer los detalles de todas las garantías del crédito.
    detalles_fiadores = DetailsGuarantees.objects.filter(
        garantia_id__credit_id=credito,
        tipo_garantia__in=["FIADOR", "CHEQUE / PAGARE"],
    ).order_by("pk")
    avalistas = []
    for detalle in detalles_fiadores:
        especificaciones = detalle.especificaciones
        if not isinstance(especificaciones, dict):
            continue
        nombre = especificaciones.get("Nombre", "")
        # Un cheque/pagaré sin una persona registrada no representa un avalista.
        if detalle.tipo_garantia == "CHEQUE / PAGARE" and not nombre:
            continue
        avalistas.append({
            "nombre": nombre,
            "dpi": especificaciones.get("DPI") or especificaciones.get("dpi", ""),
            "domicilio": especificaciones.get("Domicilio") or especificaciones.get("domicilio", ""),
        })
'''+s[b:]
s=s.replace('"incluir_aval": True if detalle_fiador else False,','"incluir_aval": bool(avalistas),\n        "avalistas": avalistas,')
s=s.replace('        "avalista_nombre": avalista_nombre,\n        "avalista_dpi": avalista_dpi,\n        "avalista_domicilio": avalista_domicilio,\n','')
s=s.replace('    if aval_info:\n        datos.update(aval_info)', '''    if aval_info:
        if "avalistas" in aval_info and "incluir_aval" not in aval_info:
            datos.pop("incluir_aval", None)
        elif "avalistas" not in aval_info and any(
            campo in aval_info for campo in ("avalista_nombre", "avalista_dpi", "avalista_domicilio")
        ):
            datos.pop("avalistas", None)
            datos.pop("incluir_aval", None)
        datos.update(aval_info)''')
s=s.replace('        Si se omite o faltan campos,', '''        avalistas: lista de diccionarios con nombre, dpi y domicilio; genera un bloque
        por persona. Una lista vacía omite el aval. incluir_aval=False lo desactiva.
        Se mantienen los campos avalista_nombre, avalista_dpi y avalista_domicilio.
        Si se omite o faltan campos,''')
p.write_text(s,encoding='utf-8')
