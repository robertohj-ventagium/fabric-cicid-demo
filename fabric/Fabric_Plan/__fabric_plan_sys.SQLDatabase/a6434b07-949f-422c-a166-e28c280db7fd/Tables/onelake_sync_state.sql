CREATE TABLE [a6434b07-949f-422c-a166-e28c280db7fd].[onelake_sync_state] (
    [id]         INT           IDENTITY (1, 1) NOT NULL,
    [name]       VARCHAR (255) NOT NULL,
    [path]       VARCHAR (450) NOT NULL,
    [syncStatus] INT           NULL,
    [createdAt]  INT           NULL,
    [updatedAt]  INT           NULL,
    CONSTRAINT [PK_onelake_sync_state] PRIMARY KEY CLUSTERED ([id] ASC),
    CONSTRAINT [UQ_onelake_sync_state_path] UNIQUE NONCLUSTERED ([path] ASC)
);


GO

