CREATE TABLE [a6434b07-949f-422c-a166-e28c280db7fd].[visual_di_3_3ac191b1b04b0bcd85053d9138a150d9] (
    [id]                         BIGINT           IDENTITY (1, 1) NOT NULL,
    [rowId]                      NVARCHAR (255)   NOT NULL,
    [colId]                      NVARCHAR (255)   NOT NULL,
    [scenarioId]                 INT              NULL,
    [filterContextHash]          NVARCHAR (255)   NULL,
    [updatedAt]                  INT              NOT NULL,
    [updatedBy]                  NVARCHAR (128)   NOT NULL,
    [dim_dim_storeStoreName]     NVARCHAR (255)   NULL,
    [dim_dim_productCategory]    NVARCHAR (255)   NULL,
    [dim_dim_productProductName] NVARCHAR (255)   NULL,
    [dim_dim_dateWeekStartDate]  NVARCHAR (255)   NULL,
    [measure_16]                 DECIMAL (30, 10) NULL,
    [measure_16_meta]            NVARCHAR (255)   NULL,
    [measure_17]                 DECIMAL (30, 10) NULL,
    [measure_17_meta]            NVARCHAR (255)   NULL,
    [measure_19]                 DECIMAL (30, 10) NULL,
    [measure_19_meta]            NVARCHAR (255)   NULL,
    [measure_21]                 DECIMAL (30, 10) NULL,
    [measure_21_meta]            NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO

