CREATE TABLE [a6434b07-949f-422c-a166-e28c280db7fd].[visual_audit_3_3ac191b1b04b0bcd85053d9138a150d9] (
    [id]                         BIGINT          IDENTITY (1, 1) NOT NULL,
    [rowId]                      NVARCHAR (2048) NOT NULL,
    [colId]                      NVARCHAR (2048) NOT NULL,
    [scenarioGuid]               NVARCHAR (255)  NULL,
    [measureGuid]                NVARCHAR (255)  NULL,
    [filterContextHash]          NVARCHAR (255)  NULL,
    [action]                     NVARCHAR (255)  NULL,
    [meta]                       NVARCHAR (MAX)  NULL,
    [oldValue]                   NVARCHAR (MAX)  NULL,
    [newValue]                   NVARCHAR (MAX)  NULL,
    [updatedAt]                  INT             NOT NULL,
    [updatedByUPN]               NVARCHAR (320)  NOT NULL,
    [updatedBy]                  NVARCHAR (128)  NOT NULL,
    [dim_dim_storeStoreName]     NVARCHAR (255)  NULL,
    [dim_dim_productCategory]    NVARCHAR (255)  NULL,
    [dim_dim_productProductName] NVARCHAR (255)  NULL,
    [dim_dim_dateWeekStartDate]  NVARCHAR (255)  NULL,
    PRIMARY KEY CLUSTERED ([id] ASC)
);


GO

