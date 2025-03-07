-- ACTUALIZACIONES

-- 1
UPDATE financings_payment SET mora = 0, capital = 3628.15 WHERE id = 189;
UPDATE financings_paymentplan SET saldo_pendiente = 27525.78  WHERE id = 90;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 3628.15 WHERE id = 12;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 3628.15, saldo_pendiente = 27525.78 WHERE id = 53;

UPDATE financings_paymentplan 
SET outstanding_balance = 27525.78, 
mora = 0, 
interest = 688.14, 
saldo_pendiente = 27525.78, 
interes_acumulado_generado = 0, 
mora_acumulado_generado = 0, 
mora_generado = 0 , 
interes_generado = 688.14
where id = 91; 

INSERT INTO financings_paymentplan (
     mes, start_date, due_date, outstanding_balance, mora, interest, principal, 
    principal_pagado, installment, status, saldo_pendiente, interes_pagado, mora_pagado, 
    fecha_limite, cambios, numero_referencia, cuota_vencida, interes_generado, 
    capital_generado, interes_acumulado_generado, mora_acumulado_generado, mora_generado, 
    paso_por_task, credit_id_id, acreedor_id, seguro_id
) VALUES (
     3, '2025-02-14 20:44:49.000000', '2025-03-14 20:44:49.000000', 27525.78, 0.00, 688.14, 0.00, 
    0.00, 5880.46, 0, 27525.78, 0.00, 0.00, 
    '2025-03-30 20:44:49.000000', 0, 'NAN', 0, 0.00, 
    5192.32, 0.00, 0.00, 0.00, 
    0, NULL, 1, NULL
);

-- 2
UPDATE financings_payment SET mora = 0, capital = 2967.11 WHERE id = 271;
UPDATE financings_paymentplan SET saldo_pendiente = 0, cuota_vencida = 0 WHERE id = 135;
DELETE FROM financings_paymentplan WHERE id = 136;

UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 2967.11 WHERE id = 27;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 2967.11, saldo_pendiente = 0 WHERE id = 83;
UPDATE accountings_creditor SET estados_fechas = 1, estado_aportacion = 1,  is_paid_off = 1,  saldo_pendiente  = 0, saldo_actual = 0 WHERE id = 24;

-- 3
UPDATE financings_payment SET mora = 0, capital = 8333.44 WHERE id = 272;
UPDATE financings_paymentplan SET saldo_pendiente = 0, cuota_vencida = 0 WHERE id = 133;
DELETE FROM financings_paymentplan WHERE id = 134;

UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 8333.44 WHERE id = 28;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 8333.44, saldo_pendiente = 0 WHERE id = 84;
UPDATE accountings_creditor SET estados_fechas = 1, estado_aportacion = 1,  is_paid_off = 1,  saldo_pendiente  = 0, saldo_actual = 0 WHERE id = 23;

-- 4
UPDATE financings_payment SET mora = 0, capital = 2292.77 WHERE id = 273;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 2292.77, saldo_pendiente = 18331.04 WHERE id = 85;
UPDATE financings_paymentplan SET saldo_pendiente = 18331.04, cuota_vencida = 0  WHERE id = 112;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 2292.77 WHERE id = 29;
UPDATE financings_paymentplan 
SET outstanding_balance = 18331.04, saldo_pendiente = 16038.63 ,interes_acumulado_generado = 0,  mora_acumulado_generado = 0, 
mora_generado = 0, interes_generado =641.59
WHERE id = 113;


UPDATE financings_payment SET mora = 0, capital = 2292.41,interes =641.59 WHERE id = 328;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 2292.41, saldo_pendiente = 16038.63 WHERE id = 109;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 2292.41,  interes =641.59, interes_pagado=641.59 WHERE id = 50;

INSERT INTO financings_paymentplan (
     mes, start_date, due_date, outstanding_balance, mora, interest, principal, 
    principal_pagado, installment, status, saldo_pendiente, interes_pagado, mora_pagado, 
    fecha_limite, cambios, numero_referencia, cuota_vencida, interes_generado, 
    capital_generado, interes_acumulado_generado, mora_acumulado_generado, mora_generado, 
    paso_por_task, credit_id_id, acreedor_id, seguro_id
) VALUES (
     3, '2025-02-10 21:40:38.000000', '2025-03-10 21:40:38.000000', 16038.63, 0.00, 561.35, 0.00, 
    0.00, 2852.88, 0, 16038.63, 561.35, 0.00, 
    '2025-03-26 21:40:38.000000', 0, 'NAN', 0, 561.35, 
    2291.53, 0.00, 0.00, 0.00, 
    0, NULL, 11, NULL
);

-- 5
UPDATE financings_payment SET mora = 0, capital = 5000 WHERE id = 277;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 5000, saldo_pendiente = 40000 WHERE id = 86;
UPDATE financings_paymentplan SET saldo_pendiente = 40000 , cuota_vencida = 0  WHERE id = 112;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 5000  WHERE id = 30;

UPDATE financings_paymentplan 
SET outstanding_balance = 40000, saldo_pendiente = 350000 ,interes_acumulado_generado = 0,  mora_acumulado_generado = 0, 
mora_generado = 0, interes_generado =1400
WHERE id = 115;


UPDATE financings_payment SET mora = 0, capital = 5000,interes =1400 WHERE id = 325;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 5000, saldo_pendiente = 35000, interest_paid = 1400 WHERE id = 108;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 5000,  interes =1400, interes_pagado=1400 WHERE id = 49;
INSERT INTO financings_paymentplan (
     mes, start_date, due_date, outstanding_balance, mora, interest, principal, 
    principal_pagado, installment, status, saldo_pendiente, interes_pagado, mora_pagado, 
    fecha_limite, cambios, numero_referencia, cuota_vencida, interes_generado, 
    capital_generado, interes_acumulado_generado, mora_acumulado_generado, mora_generado, 
    paso_por_task, credit_id_id, acreedor_id, seguro_id
) VALUES (
    , 3, '2025-02-09 15:48:29.000000', '2025-03-09 15:48:29.000000', 35000.00, 0.00, 1225.00, 0.00, 
    0.00, 6225.00, 0, 35000.00, 0.00, 0.00, 
    '2025-03-25 15:48:29.000000', 0, 'NAN', 0, 1225.00, 
    5000.00, 0.00, 0.00, 0.00, 
    0, NULL, 12, NULL
);

-- 6
UPDATE financings_payment SET mora = 0, capital = 500 WHERE id = 278;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 500, saldo_pendiente = 3000 WHERE id = 87;
UPDATE financings_paymentplan SET saldo_pendiente = 3000 , cuota_vencida = 0  WHERE id = 116;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 500  WHERE id = 31;

UPDATE financings_paymentplan 
SET outstanding_balance = 3000, saldo_pendiente = 2500 ,interes_acumulado_generado = 0,  mora_acumulado_generado = 0, 
mora_generado = 0, interes_generado =300
WHERE id = 117;


UPDATE financings_payment SET mora = 0, capital = 500,interes =300 WHERE id = 330;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 500, saldo_pendiente = 2500, interest_paid = 300 WHERE id = 111;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 500,  interes =300, interes_pagado=300 WHERE id = 51;

INSERT INTO financings_paymentplan (
    mes, start_date, due_date, outstanding_balance, mora, interest, principal, 
    principal_pagado, installment, status, saldo_pendiente, interes_pagado, mora_pagado, 
    fecha_limite, cambios, numero_referencia, cuota_vencida, interes_generado, 
    capital_generado, interes_acumulado_generado, mora_acumulado_generado, mora_generado, 
    paso_por_task, credit_id_id, acreedor_id, seguro_id
) VALUES (
     3, '2025-02-10 16:39:10.000000', '2025-03-10 16:39:10.000000', 2500.00, 0.00, 250.00, 0.00, 
    0.00, 750.00, 0, 0.00, 0.00, 0.00, 
    '2025-03-26 16:39:10.000000', 0, 'NAN', 0, 250.00, 
    500.00, 0.00, 0.00, 0.00, 
    0, NULL, 13, NULL
);

-- 7
UPDATE financings_payment SET mora = 0, capital = 2500.04 WHERE id = 280;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 2500.04, saldo_pendiente = 2499.46 WHERE id = 89;
UPDATE financings_paymentplan SET saldo_pendiente = 2499.46 , cuota_vencida = 0  WHERE id = 116;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 2499.46  WHERE id = 33;
UPDATE financings_paymentplan
SET outstanding_balance = 2499.46, saldo_pendiente = 0 ,interes_acumulado_generado = 0,  mora_acumulado_generado = 0,
mora_generado = 0, interes_generado =187.46
WHERE id = 123;


UPDATE financings_payment SET mora = 0, capital = 2500.54,interes =187.46 WHERE id = 331;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 2500.54, saldo_pendiente = 0, interest_paid = 187.46 WHERE id = 112;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 2500.54,  interes =187.46, interes_pagado=187.46 WHERE id = 52;
UPDATE accountings_creditor SET estados_fechas = 1, estado_aportacion = 1,  is_paid_off = 1,  saldo_pendiente  = 0, saldo_actual = 0 WHERE id = 16;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 2500.04  WHERE id = 33;
