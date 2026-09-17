CREATE TABLE [d359507c-91ba-4dac-85a8-1c7c862bbedb].[visual_di_2_6fa000f07fb5b4ba0cde6f6785500c06] (
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
    [measure_11]                    DECIMAL (30, 10) NULL,
    [measure_12]                    DECIMAL (30, 10) NULL,
    [measure_13]                    NVARCHAR (MAX)   NULL,
    [measure_19]                    NVARCHAR (255)   NULL,
    [measure_20]                    NVARCHAR (255)   NULL,
    [measure_11_meta]               NVARCHAR (255)   NULL,
    [measure_12_meta]               NVARCHAR (255)   NULL,
    [measure_13_meta]               NVARCHAR (255)   NULL,
    [measure_19_meta]               NVARCHAR (255)   NULL,
    [measure_20_meta]               NVARCHAR (255)   NULL,
    PRIMARY KEY CLUSTERED ([id] ASC),
    UNIQUE NONCLUSTERED ([rowId] ASC, [colId] ASC, [scenarioId] ASC, [filterContextHash] ASC)
);


GO

