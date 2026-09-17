CREATE TABLE [ff0a9f2b-a2de-423e-aec7-20903c1daf57].[visual_di_1_51166426bc296cf0938bddc5e8833985] (
    [id]                            BIGINT           IDENTITY (1, 1) NOT NULL,
    [rowId]                         NVARCHAR (255)   NOT NULL,
    [colId]                         NVARCHAR (255)   NOT NULL,
    [scenarioId]                    INT              NULL,
    [filterContextHash]             NVARCHAR (255)   NULL,
    [updatedAt]                     INT              NOT NULL,
    [updatedBy]                     NVARCHAR (128)   NOT NULL,
    [dim_DimAccountHierarchyLevel1] NVARCHAR (255)   NULL,
    [dim_DimAccountHierarchyLevel2] NVARCHAR (255)   NULL,
    [dim_DimAccountHierarchyLevel3] NVARCHAR (255)   NULL,
    [dim_DimAccountHierarchyLevel4] NVARCHAR (255)   NULL,
    [dim_DimAccountHierarchyLevel5] NVARCHAR (255)   NULL,
    [dim_DimAccountHierarchyLevel6] NVARCHAR (255)   NULL,
    [dim_DimAccountAccountKey]      NVARCHAR (255)   NULL,
    [dim_DimDateCalendarYear]       NVARCHAR (255)   NULL,
    [dim_DimDateCalendarQuarter]    NVARCHAR (255)   NULL,
    [measure_1]                     DECIMAL (30, 10) NULL,
    [measure_7]                     DECIMAL (30, 10) NULL,
    [measure_12]                    DECIMAL (30, 10) NULL,
    [measure_13]                    NVARCHAR (MAX)   NULL,
    [measure_19]                    NVARCHAR (255)   NULL,
    [measure_20]                    NVARCHAR (255)   NULL,
    [measure_1_meta]                NVARCHAR (255)   NULL,
    [measure_7_meta]                NVARCHAR (255)   NULL,
    [measure_12_meta]               NVARCHAR (255)   NULL,
    [measure_13_meta]               NVARCHAR (255)   NULL,
    [measure_19_meta]               NVARCHAR (255)   NULL,
    [measure_20_meta]               NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO

