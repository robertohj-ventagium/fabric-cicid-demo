CREATE TABLE [09d5e4a3-e62b-49dc-9960-d50b187c838a].[visual_di_3_c352efe12e7ec5a4756721e3c43fc122] (
    [id]                         BIGINT           IDENTITY (1, 1) NOT NULL,
    [rowId]                      NVARCHAR (255)   NOT NULL,
    [colId]                      NVARCHAR (255)   NOT NULL,
    [scenarioId]                 INT              NULL,
    [filterContextHash]          NVARCHAR (255)   NULL,
    [updatedAt]                  INT              NOT NULL,
    [updatedBy]                  NVARCHAR (128)   NOT NULL,
    [dim_dim_productCategory]    NVARCHAR (255)   NULL,
    [dim_dim_productSubcategory] NVARCHAR (255)   NULL,
    [dim_dim_productSKU]         NVARCHAR (255)   NULL,
    [dim_dim_dateMonthYear]      NVARCHAR (255)   NULL,
    [measure_10]                 DECIMAL (30, 10) NULL,
    [measure_10_meta]            NVARCHAR (255)   NULL,
    [measure_12]                 DECIMAL (30, 10) NULL,
    [measure_12_meta]            NVARCHAR (255)   NULL,
    [measure_13]                 DECIMAL (30, 10) NULL,
    [measure_13_meta]            NVARCHAR (255)   NULL,
    [measure_21]                 NVARCHAR (255)   NULL,
    [measure_21_meta]            NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO

