CREATE TABLE [09d5e4a3-e62b-49dc-9960-d50b187c838a].[visual_di_8_98a73d23b4dde89d9c452eeb3318635e] (
    [id]                      BIGINT           IDENTITY (1, 1) NOT NULL,
    [rowId]                   NVARCHAR (255)   NOT NULL,
    [colId]                   NVARCHAR (255)   NOT NULL,
    [scenarioId]              INT              NULL,
    [filterContextHash]       NVARCHAR (255)   NULL,
    [updatedAt]               INT              NOT NULL,
    [updatedBy]               NVARCHAR (128)   NOT NULL,
    [dim_dim_productCategory] NVARCHAR (255)   NULL,
    [measure_18]              DECIMAL (30, 10) NULL,
    [measure_19]              DECIMAL (30, 10) NULL,
    [measure_20]              DECIMAL (30, 10) NULL,
    [measure_18_meta]         NVARCHAR (255)   NULL,
    [measure_19_meta]         NVARCHAR (255)   NULL,
    [measure_20_meta]         NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO

