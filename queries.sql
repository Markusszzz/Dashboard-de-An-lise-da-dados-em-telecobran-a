-- ============================================================
--  DEBT ANALYTICS DASHBOARD — SQL Queries
--  Base: cobranca_dados.csv (importada como tabela "cobranca")
-- ============================================================


-- 1. VISÃO GERAL — KPIs principais
SELECT
    COUNT(*)                                        AS total_clientes,
    SUM(CASE WHEN Status != 'PAGO' THEN 1 ELSE 0 END) AS inadimplentes,
    SUM(Valor_Pago)                                 AS total_recuperado,
    ROUND(SUM(Valor_Pago) / SUM(Valor_Divida) * 100, 1) AS taxa_recuperacao_pct,
    ROUND(AVG(CASE WHEN Status != 'PAGO' THEN Dias_Atraso END), 0) AS media_dias_atraso,
    SUM(CASE WHEN Status IN ('PAGO','NEGOCIANDO') THEN 1 ELSE 0 END) AS acordos_fechados
FROM cobranca;


-- 2. CLIENTES POR FAIXA DE ATRASO
SELECT
    Faixa_Atraso,
    COUNT(*)              AS qtd_clientes,
    ROUND(AVG(Valor_Divida), 2) AS ticket_medio,
    SUM(Valor_Divida)     AS total_em_aberto
FROM cobranca
WHERE Status != 'PAGO'
GROUP BY Faixa_Atraso
ORDER BY MIN(Dias_Atraso);


-- 3. TOP INADIMPLENTES — maior saldo devedor
SELECT
    ID,
    Nome,
    CPF,
    Telefone,
    Valor_Divida,
    Dias_Atraso,
    Valor_Pago,
    (Valor_Divida - Valor_Pago) AS saldo_devedor,
    Status,
    Operador,
    CASE
        WHEN Dias_Atraso > 90 THEN 'CRÍTICO'
        WHEN Dias_Atraso > 60 THEN 'ALTO'
        WHEN Dias_Atraso > 30 THEN 'MÉDIO'
        ELSE                       'BAIXO'
    END AS nivel_risco
FROM cobranca
WHERE Status != 'PAGO'
ORDER BY saldo_devedor DESC
LIMIT 50;


-- 4. RECUPERAÇÃO POR OPERADOR (ranking)
SELECT
    Operador,
    COUNT(*)                                             AS total_clientes,
    SUM(CASE WHEN Status = 'PAGO' THEN 1 ELSE 0 END)   AS total_pagos,
    ROUND(SUM(CASE WHEN Status = 'PAGO' THEN 1.0 ELSE 0 END)
          / COUNT(*) * 100, 1)                           AS taxa_pct,
    SUM(Valor_Pago)                                      AS valor_recuperado
FROM cobranca
GROUP BY Operador
ORDER BY taxa_pct DESC;


-- 5. STATUS DOS ACORDOS
SELECT
    Status,
    COUNT(*)          AS qtd,
    SUM(Valor_Pago)   AS valor_recuperado
FROM cobranca
GROUP BY Status
ORDER BY qtd DESC;


-- 6. CARTEIRA TOTAL vs EM RISCO
SELECT
    SUM(Valor_Divida)                                   AS carteira_total,
    SUM(CASE WHEN Dias_Atraso > 60 THEN Valor_Divida ELSE 0 END) AS carteira_risco,
    SUM(Valor_Pago)                                     AS total_recuperado,
    SUM(Valor_Divida) - SUM(Valor_Pago)                 AS total_em_aberto
FROM cobranca;
