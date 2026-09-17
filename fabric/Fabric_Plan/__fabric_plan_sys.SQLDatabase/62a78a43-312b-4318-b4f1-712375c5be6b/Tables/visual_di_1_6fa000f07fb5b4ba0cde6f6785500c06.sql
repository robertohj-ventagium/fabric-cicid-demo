CREATE TABLE [62a78a43-312b-4318-b4f1-712375c5be6b].[visual_di_1_6fa000f07fb5b4ba0cde6f6785500c06] (
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
    [dim_DimDateCalendarYear]       NVARCHAR (255)   NULL,
    [dim_DimDateCalendarQuarter]    NVARCHAR (255)   NULL,
    [measure_1]                     DECIMAL (30, 10) NULL,
    [measure_1_meta]                NVARCHAR (255)   NULL,
    [measure_2]                     DECIMAL (30, 10) NULL,
    [measure_2_meta]                NVARCHAR (255)   NULL,
    [measure_3]                     NVARCHAR (MAX)   NULL,
    [measure_3_meta]                NVARCHAR (255)   NULL,
    [measure_4]                     NVARCHAR (255)   NULL,
    [measure_4_meta]                NVARCHAR (255)   NULL,
    [measure_5]                     NVARCHAR (255)   NULL,
    [measure_5_meta]                NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO

