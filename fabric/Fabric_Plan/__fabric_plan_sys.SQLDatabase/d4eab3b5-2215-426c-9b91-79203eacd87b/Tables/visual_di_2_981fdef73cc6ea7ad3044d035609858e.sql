CREATE TABLE [d4eab3b5-2215-426c-9b91-79203eacd87b].[visual_di_2_981fdef73cc6ea7ad3044d035609858e] (
    [id]                      BIGINT           IDENTITY (1, 1) NOT NULL,
    [rowId]                   NVARCHAR (255)   NOT NULL,
    [colId]                   NVARCHAR (255)   NOT NULL,
    [scenarioId]              INT              NULL,
    [filterContextHash]       NVARCHAR (255)   NULL,
    [updatedAt]               INT              NOT NULL,
    [updatedBy]               NVARCHAR (128)   NOT NULL,
    [dim_dim_productCategory] NVARCHAR (255)   NULL,
    [dim_dim_storeRegion]     NVARCHAR (255)   NULL,
    [dim_dim_dateMonthYear]   NVARCHAR (255)   NULL,
    [measure_1]               DECIMAL (30, 10) NULL,
    [measure_2]               DECIMAL (30, 10) NULL,
    [measure_1_meta]          NVARCHAR (255)   NULL,
    [measure_2_meta]          NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO

