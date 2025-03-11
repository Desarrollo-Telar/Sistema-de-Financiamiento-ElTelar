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