CREATE TABLE [62a78a43-312b-4318-b4f1-712375c5be6b].[visual_audit_1_6fa000f07fb5b4ba0cde6f6785500c06] (
    [id]                            BIGINT          IDENTITY (1, 1) NOT NULL,
    [rowId]                         NVARCHAR (2048) NOT NULL,
    [colId]                         NVARCHAR (2048) NOT NULL,
    [scenarioGuid]                  NVARCHAR (255)  NULL,
    [measureGuid]                   NVARCHAR (255)  NULL,
    [filterContextHash]             NVARCHAR (255)  NULL,
    [action]                        NVARCHAR (255)  NULL,
    [meta]                          NVARCHAR (MAX)  NULL,
    [oldValue]                      NVARCHAR (MAX)  NULL,
    [newValue]                      NVARCHAR (MAX)  NULL,
    [updatedAt]                     INT             NOT NULL,
    [updatedByUPN]                  NVARCHAR (320)  NOT NULL,
    [updatedBy]                     NVARCHAR (128)  NOT NULL,
    [dim_DimAccountHierarchyLevel1] NVARCHAR (255)  NULL,
    [dim_DimAccountHierarchyLevel2] NVARCHAR (255)  NULL,
    [dim_DimAccountHierarchyLevel3] NVARCHAR (255)  NULL,
    [dim_DimAccountHierarchyLevel4] NVARCHAR (255)  NULL,
    [dim_DimAccountHierarchyLevel5] NVARCHAR (255)  NULL,
    [dim_DimDateCalendarYear]       NVARCHAR (255)  NULL,
    [dim_DimDateCalendarQuarter]    NVARCHAR (255)  NULL,
    PRIMARY KEY CLUSTERED ([id] ASC)
);


GO

