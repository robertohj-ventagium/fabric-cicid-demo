CREATE TABLE [d4eab3b5-2215-426c-9b91-79203eacd87b].[allocations_user_access] (
    [id]                   INT           IDENTITY (1, 1) NOT NULL,
    [visualId]             INT           NULL,
    [accessEntityType]     INT           NULL,
    [accessEntityId]       VARCHAR (128) NULL,
    [accessPermissionType] INT           NULL,
    [createdBy]            VARCHAR (128) NULL,
    [updatedBy]            VARCHAR (128) NULL,
    [createdAt]            INT           NULL,
    [updatedAt]            INT           NULL,
    CONSTRAINT [PK_allocations_user_access] PRIMARY KEY CLUSTERED ([id] ASC)
);


GO

