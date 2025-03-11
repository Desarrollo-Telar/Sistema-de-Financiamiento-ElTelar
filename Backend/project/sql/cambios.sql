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

-- 8
UPDATE financings_payment SET mora = 0, capital = 8327.96 WHERE id = 283;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 8327.96, saldo_pendiente = 0 WHERE id = 92;
UPDATE financings_paymentplan SET saldo_pendiente = 0 , cuota_vencida = 0  WHERE id = 131;
DELETE FROM financings_paymentplan WHERE id = 132;
UPDATE accountings_creditor SET estados_fechas = 1, estado_aportacion = 1,  is_paid_off = 1,  saldo_pendiente  = 0, saldo_actual = 0 WHERE id = 22;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 8327.96  WHERE id = 36;

-- 9
UPDATE financings_payment SET mora = 0, capital = 1833.44 WHERE id = 292;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 1833.44, saldo_pendiente = 0 WHERE id = 93;
UPDATE financings_paymentplan SET saldo_pendiente = 0 , cuota_vencida = 0  WHERE id = 137;
DELETE FROM financings_paymentplan WHERE id = 138;
UPDATE accountings_creditor SET estados_fechas = 1, estado_aportacion = 1,  is_paid_off = 1,  saldo_pendiente  = 0, saldo_actual = 0 WHERE id = 25;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 1833.44  WHERE id = 37;

-- 10
UPDATE financings_payment SET mora = 0, capital = 1250 WHERE id = 293;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 1250, saldo_pendiente = 8750 WHERE id = 94;
UPDATE financings_paymentplan SET saldo_pendiente = 8750 , cuota_vencida = 0  WHERE id = 110;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 1250 WHERE id = 38;

UPDATE financings_paymentplan 
SET outstanding_balance = 8750, 
mora = 0, 
interest = 525, 
saldo_pendiente = 8750, 
interes_acumulado_generado = 0, 
mora_acumulado_generado = 0, 
mora_generado = 0 , 
interes_generado = 525
where id = 111; 

INSERT INTO financings_paymentplan (
     mes, start_date, due_date, outstanding_balance, mora, interest, principal, 
    principal_pagado, installment, status, saldo_pendiente, interes_pagado, mora_pagado, 
    fecha_limite, cambios, numero_referencia, cuota_vencida, interes_generado, 
    capital_generado, interes_acumulado_generado, mora_acumulado_generado, mora_generado, 
    paso_por_task, credit_id_id, acreedor_id, seguro_id
) VALUES (
     3, '2025-02-14 14:08:15.000000', '2025-03-14 14:08:15.000000', 8750.00, 0.00, 525.00, 0.00, 
    0.00, 1775.00, 0, 8750.00, 0.00, 0.00, 
    '2025-03-30 14:08:15.000000', 0, 'NAN', 0, 525.00, 
    1250.00, 0.00, 0.00, 0.00, 
    0, NULL, 10, NULL
);

-- 11
UPDATE financings_payment SET mora = 0, capital = 833.73 WHERE id = 300;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 833.73, saldo_pendiente = 3336.95 WHERE payment_id = 300;
UPDATE financings_paymentplan SET saldo_pendiente = 3336.95  , cuota_vencida = 0  WHERE id = 92;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 833.73 WHERE pago_id = 300;

UPDATE financings_payment SET mora = 0, , interes = 83.42, capital = 833.58 WHERE id = 385;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 833.58, saldo_pendiente = 2503.37, interest_paid=83.42 WHERE payment_id = 385;

UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 833.58, interes=83.42,interes_pagado=83.42 WHERE pago_id = 385;

UPDATE financings_paymentplan 
SET outstanding_balance = 3336.95, 
mora = 0, 
interest = 0, 
saldo_pendiente = 2503.37, 
interes_acumulado_generado = 0, 
mora_acumulado_generado = 0, 
mora_generado = 0 , 
interes_generado = 83.42
where id = 93; 



-- 12
UPDATE financings_payment SET mora = 0, capital = 1512.66 WHERE id = 301;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 1512.66, saldo_pendiente = 5501.12 WHERE payment_id = 301;
UPDATE financings_paymentplan SET saldo_pendiente = 5501.12 , cuota_vencida = 0  WHERE id = 94;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 1512.66 WHERE pago_id = 301;

UPDATE financings_paymentplan 
SET outstanding_balance = 5501.12, 
mora = 0, 
interest = 137.53, 
saldo_pendiente = 5501.12, 
interes_acumulado_generado = 0, 
mora_acumulado_generado = 0, 
mora_generado = 0 , 
interes_generado = 137.53
where id = 95; 

-- 13
UPDATE financings_payment SET mora = 0, capital = 4178.53 WHERE id = 302;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 4178.53 , saldo_pendiente = 20244.97 WHERE payment_id = 302;
UPDATE financings_paymentplan SET saldo_pendiente = 20244.97 , cuota_vencida = 0  WHERE id = 102;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 4178.53  WHERE pago_id = 302;

UPDATE financings_paymentplan 
SET outstanding_balance = 20244.97, 
mora = 0, 
interest = 404.9, 
saldo_pendiente = 20244.97, 
interes_acumulado_generado = 0, 
mora_acumulado_generado = 0, 
mora_generado = 0 , 
interes_generado = 404.9
where id = 103; 

-- 14
UPDATE financings_payment SET mora = 0, capital = 4144.36 WHERE id = 303;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 4144.36 , saldo_pendiente = 21987.59 WHERE payment_id = 303;
UPDATE financings_paymentplan SET saldo_pendiente = 21987.59 , cuota_vencida = 0  WHERE id = 104;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 4144.36  WHERE pago_id = 303;

UPDATE financings_paymentplan 
SET outstanding_balance = 21987.59, 
mora = 0, 
interest = 439.75, 
saldo_pendiente = 21987.59, 
interes_acumulado_generado = 0, 
mora_acumulado_generado = 0, 
mora_generado = 0 , 
interes_generado = 439.75
where id = 105; 

-- 15
UPDATE financings_payment SET mora = 0, capital = 1255.12 WHERE id = 304;
UPDATE financings_accountstatement SET late_fee_paid = 0, capital_paid = 1255.12 , saldo_pendiente = 626305.51 WHERE payment_id = 304;
UPDATE financings_paymentplan SET saldo_pendiente = 626305.51  , cuota_vencida = 0  WHERE id = 98;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 1255.12  WHERE pago_id = 304;

UPDATE financings_paymentplan 
SET outstanding_balance = 626305.51 , 
mora = 0, 
interest = 12526.11, 
saldo_pendiente = 626305.51 , 
interes_acumulado_generado = 0, 
mora_acumulado_generado = 0, 
mora_generado = 0 , 
interes_generado = 12526.11
where id = 99; 

-- 16
INSERT INTO financings_paymentplan (
    mes, start_date, due_date, outstanding_balance, mora, interest, principal, 
    principal_pagado, installment, status, saldo_pendiente, interes_pagado, mora_pagado, 
    fecha_limite, cambios, numero_referencia, cuota_vencida, interes_generado, 
    capital_generado, interes_acumulado_generado, mora_acumulado_generado, mora_generado, 
    paso_por_task, credit_id_id, acreedor_id, seguro_id
) VALUES (
     3, '2025-02-05 14:58:46.000000', '2025-03-05 14:58:46.000000', 15542.64, 0.00, 388.57, 0.00, 
    0.00, 2888.42, 0, 15542.64, 0.00, 0.00, 
    '2025-03-21 14:58:46.000000', 0, 'NAN', 0, 388.57, 
    2499.85, 0.00, 0.00, 0.00, 
    0, NULL, 8, NULL
);

-- 17

INSERT INTO financings_paymentplan (
     mes, start_date, due_date, outstanding_balance, mora, interest, principal, 
    principal_pagado, installment, status, saldo_pendiente, interes_pagado, mora_pagado, 
    fecha_limite, cambios, numero_referencia, cuota_vencida, interes_generado, 
    capital_generado, interes_acumulado_generado, mora_acumulado_generado, mora_generado, 
    paso_por_task, credit_id_id, acreedor_id, seguro_id
) VALUES (
     3, '2025-02-05 15:03:30.000000', '2025-03-05 15:03:30.000000', 20722.47, 0.00, 518.06, 0.00, 
    0.00, 3851.14, 0, 20722.47, 0.00, 0.00, 
    '2025-03-21 15:03:30.000000', 0, 'NAN', 0, 518.06, 
    3333.08, 0.00, 0.00, 0.00, 
    0, NULL, 9, NULL
);

-- 18
INSERT INTO financings_paymentplan (
   mes, start_date, due_date, outstanding_balance, mora, interest, principal, 
    principal_pagado, installment, status, saldo_pendiente, interes_pagado, mora_pagado, 
    fecha_limite, cambios, numero_referencia, cuota_vencida, interes_generado, 
    capital_generado, interes_acumulado_generado, mora_acumulado_generado, mora_generado, 
    paso_por_task, credit_id_id, acreedor_id, seguro_id
) VALUES (
     3, '2025-02-15 15:58:48.000000', '2025-03-15 15:58:48.000000', 954.00, 0.00, 0.00, 0.00, 
    0.00, 318.00, 0, 954.00, 0.00, 0.00, 
    '2025-03-31 15:58:48.000000', 0, 'NAN', 0, 0.00, 
    318.00, 0.00, 0.00, 0.00, 
    0, NULL, NULL, 1
);

-- 19
UPDATE financings_payment SET mora = 0, capital = 830.18 WHERE id = 367;

UPDATE financings_accountstatement 
SET late_fee_paid = 0, capital_paid = 830.18 , saldo_pendiente = 9260.82, abono=1587 
WHERE payment_id = 367;

UPDATE financings_paymentplan SET saldo_pendiente = 9260.82  , cuota_vencida = 0  WHERE id = 178;
UPDATE financings_recibo SET mora = 0, mora_pagada = 0, aporte_capital = 9260.82, total = 1587 WHERE pago_id = 367;


-- 20
UPDATE financings_accountstatement 
SET  saldo_pendiente = 23900.92
WHERE id = 147;

UPDATE financings_paymentplan SET saldo_pendiente = 23900.92 , cuota_vencida = 0  WHERE id = 91;

UPDATE financings_paymentplan 
SET outstanding_balance =  23900.92  , 
mora = 0, 
interest = 597.52, 
saldo_pendiente =  23900.92  , 
interes_acumulado_generado = 0, 
mora_acumulado_generado = 0, 
mora_generado = 0 , 
interes_generado = 597.52
where id = 189; 

-- 21
UPDATE financings_accountstatement 
SET saldo_pendiente = 3988.65
WHERE payment_id = 380;

UPDATE financings_paymentplan SET saldo_pendiente = 3988.65, cuota_vencida = 0  WHERE id = 95;

-- 22
UPDATE financings_accountstatement 
SET saldo_pendiente = 625831.62
WHERE payment_id = 391;

UPDATE financings_paymentplan SET saldo_pendiente = 625831.62, cuota_vencida = 0  WHERE id = 99;
