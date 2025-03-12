-- 4
UPDATE financings_payment
SET interes = 12551.21, capital = 448.79
WHERE id = 304;

UPDATE financings_accountstatement 
SET late_fee_paid = 0, 
interest_paid = 12551.21,
capital_paid = 448.79 , 
saldo_pendiente = 627111.84
WHERE payment_id = 304;

UPDATE financings_paymentplan SET saldo_pendiente = 627111.84  , cuota_vencida = 0  WHERE id = 98;
UPDATE financings_recibo 
SET mora = 0, mora_pagada = 0, 
aporte_capital = 448.79,  interes_pagado=12551.21, 
interes=12551.21 
WHERE pago_id = 304;

--
UPDATE financings_payment
SET interes = 12542.24, capital = 457.76
WHERE id = 391;

UPDATE financings_accountstatement 
SET late_fee_paid = 0, 
interest_paid = 12542.24,
capital_paid = 457.76 , 
saldo_pendiente = 626654.08
WHERE payment_id = 391;


UPDATE financings_recibo 
SET mora = 0, mora_pagada = 0, 
aporte_capital = 457.76,  interes_pagado=12542.24, 
interes=12542.24
WHERE pago_id = 391;

UPDATE financings_paymentplan 
SET outstanding_balance = 627111.84 , 
mora = 0, 
interest = 0, 
saldo_pendiente = 626654.08 , 
interes_acumulado_generado = 0, 
mora_acumulado_generado = 0, 
mora_generado = 0 , 
interes_generado = 12542.24
where id = 99; 

--2
UPDATE financings_accountstatement 
SET saldo_pendiente = 16065.87
WHERE payment_id = 389;

UPDATE financings_paymentplan SET saldo_pendiente = 16065.87, cuota_vencida = 0  WHERE id = 103;
-- 3
UPDATE financings_accountstatement 
SET saldo_pendiente = 17843.34
WHERE payment_id = 399;

UPDATE financings_paymentplan SET saldo_pendiente = 17843.34, cuota_vencida = 0  WHERE id = 105;
-- 4
UPDATE financings_accountstatement 
SET saldo_pendiente = 7500
WHERE payment_id = 404;

UPDATE financings_paymentplan SET saldo_pendiente =  7500, cuota_vencida = 0  WHERE id = 192;

--5 
UPDATE financings_payment
SET  capital =2292.17
WHERE id = 273;

UPDATE financings_accountstatement 
SET late_fee_paid = 0, 
capital_paid = 2292.17 , 
saldo_pendiente = 18331.64
WHERE payment_id = 273;

UPDATE financings_paymentplan SET saldo_pendiente = 18331.64  , cuota_vencida = 0  WHERE id = 112;
UPDATE financings_recibo 
SET mora = 0, mora_pagada = 0, 
aporte_capital = 2292.17
WHERE pago_id = 273;

--
UPDATE financings_payment
SET  capital =2292.39, interes = 641.61
WHERE id = 328;

UPDATE financings_accountstatement 
SET late_fee_paid = 0, 
capital_paid = 2292.39 , 
saldo_pendiente = 16039.25,
interest_paid = 641.61
WHERE payment_id = 328;

UPDATE financings_paymentplan SET saldo_pendiente = 16039.25  , cuota_vencida = 0  WHERE id = 113;

UPDATE financings_recibo 
SET mora = 0, mora_pagada = 0, 
aporte_capital = 2292.39,  interes_pagado=641.61, 
interes=641.61
WHERE pago_id = 328;

UPDATE financings_paymentplan 
SET saldo_pendiente = 16039.25  , outstanding_balance=16039.25 , 
interest = 561.37, interes_generado = 561.37,
cuota_vencida = 0  
WHERE id = 190;

-- 6

UPDATE accountings_creditor
SET numero_referencia = "1739416972"
WHERE id = 9;

DELETE FROM financings_accountstatement 
WHERE numero_referencia = '837643467';

DELETE FROM financings_recibo
WHERE pago_id IN (
    SELECT id FROM financings_payment WHERE numero_referencia = '837643467'
);

UPDATE financings_payment
SET estado_transaccion = "PENDIENTE",
monto = 3917.00
WHERE numero_referencia = "837643467";



-- 7
UPDATE accountings_creditor
SET numero_referencia = "1707975966"
WHERE id = 8;



DELETE FROM financings_accountstatement 
WHERE numero_referencia = "837593994";

DELETE FROM financings_recibo
WHERE pago_id IN (
    SELECT id FROM financings_payment WHERE numero_referencia = '837593994'
);



UPDATE financings_payment
SET estado_transaccion = "PENDIENTE",
monto = 2938.00
WHERE numero_referencia = "837593994";

-- 8

UPDATE financings_payment
SET interes = 437.47, capital = 2500.53, mora = 0
WHERE numero_referencia = "837593994";

UPDATE financings_accountstatement 
SET late_fee_paid = 0, 
interest_paid = 437.47,
capital_paid = 2500.53 , 
saldo_pendiente = 14998.42
WHERE payment_id  IN (
    SELECT id FROM financings_payment WHERE numero_referencia = '837593994'
);


UPDATE financings_paymentplan SET saldo_pendiente = 14998.42  , cuota_vencida = 0  WHERE numero_referencia = '837593994';

UPDATE financings_recibo 
SET mora = 0, mora_pagada = 0, 
aporte_capital = 2500.53,  interes_pagado=437.47, 
interes=437.47 
WHERE pago_id IN (
    SELECT id FROM financings_payment WHERE numero_referencia = '837593994'
);


--

UPDATE financings_payment
SET interes = 374.96, capital = 2500.04, mora = 0
WHERE numero_referencia = "1734063844";

UPDATE financings_accountstatement 
SET late_fee_paid = 0, 
interest_paid = 374.96,
capital_paid = 2500.04 , 
saldo_pendiente = 12498.38
WHERE payment_id  IN (
    SELECT id FROM financings_payment WHERE numero_referencia = '1734063844'
);


UPDATE financings_paymentplan 
SET saldo_pendiente = 12498.38 , cuota_vencida = 0, 
mora=0,  mora_acumulado_generado = 0,
mora_generado = 0, interes_generado = 374.96
WHERE numero_referencia = '1734063844';

UPDATE financings_recibo 
SET mora = 0, mora_pagada = 0, 
aporte_capital = 2500.04,  interes_pagado=374.96, 
interes=374.96
WHERE pago_id IN (
    SELECT id FROM financings_payment WHERE numero_referencia = '1734063844'
);