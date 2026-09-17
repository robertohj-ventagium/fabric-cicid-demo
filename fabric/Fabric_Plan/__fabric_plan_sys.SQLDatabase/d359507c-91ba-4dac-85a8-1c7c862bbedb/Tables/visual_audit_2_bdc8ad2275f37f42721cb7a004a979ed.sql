CREATE TABLE [d359507c-91ba-4dac-85a8-1c7c862bbedb].[visual_audit_2_bdc8ad2275f37f42721cb7a004a979ed] (
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
    [dim_DimAccountHierarchyLevel6] NVARCHAR (255)  NULL,
    [dim_DimDateCalendarYear]       NVARCHAR (255)  NULL,
    [dim_DimDateCalendarQuarter]    NVARCHAR (255)  NULL,
    PRIMARY KEY CLUSTERED ([id] ASC)
);


GO

