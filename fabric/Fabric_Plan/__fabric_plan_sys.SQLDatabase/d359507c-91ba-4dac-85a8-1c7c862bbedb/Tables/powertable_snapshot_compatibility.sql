CREATE TABLE [d359507c-91ba-4dac-85a8-1c7c862bbedb].[powertable_snapshot_compatibility] (
    [id]                             INT            IDENTITY (1, 1) NOT NULL,
    [sourceId]                       INT            NOT NULL,
    [sourceSnapshotSchemaData]       NVARCHAR (MAX) NULL,
    [sourceSnapshotColumnConfigData] NVARCHAR (MAX) NULL,
    [sourceSnapshotId]               INT            NULL,
    [targetSnapshotId]               INT            NOT NULL,
    [compatibilityStatus]            INT            NOT NULL,
    [compatibilityIssues]            NVARCHAR (MAX) NULL,
    [status]                         INT            NOT NULL,
    [createdAt]                      INT            NOT NULL,
    [updatedAt]                      INT            NOT NULL,
    [createdBy]                      NVARCHAR (128) NOT NULL,
    [updatedBy]                      NVARCHAR (128) NOT NULL,
    CONSTRAINT [PK_679489b8dcdf6deb5c7697e67f1] PRIMARY KEY CLUSTERED ([id] ASC),
    CONSTRAINT [FK_compat_powertable_source] FOREIGN KEY ([sourceId]) REFERENCES [d359507c-91ba-4dac-85a8-1c7c862bbedb].[powertable_source] ([id]),
    CONSTRAINT [FK_compat_targetSnapshot] FOREIGN KEY ([targetSnapshotId]) REFERENCES [d359507c-91ba-4dac-85a8-1c7c862bbedb].[powertable_snapshot] ([id])
);


GO

