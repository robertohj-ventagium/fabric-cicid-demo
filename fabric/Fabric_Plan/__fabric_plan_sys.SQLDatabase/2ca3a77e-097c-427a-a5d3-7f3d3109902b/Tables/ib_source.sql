CREATE TABLE [2ca3a77e-097c-427a-a5d3-7f3d3109902b].[ib_source] (
    [id]             INT            IDENTITY (1, 1) NOT NULL,
    [type]           INT            NOT NULL,
    [meta]           NVARCHAR (MAX) NOT NULL,
    [workloadItemId] NVARCHAR (36)  NOT NULL,
    [visualId]       INT            NULL,
    [name]           VARCHAR (2048) NOT NULL,
    [filePath]       VARCHAR (255)  NULL,
    [status]         INT            CONSTRAINT [DF_208052c910ea47b876840dd43dd] DEFAULT ((10)) NOT NULL,
    [createdBy]      NVARCHAR (128) NOT NULL,
    [updatedBy]      NVARCHAR (128) NOT NULL,
    [createdAt]      INT            NOT NULL,
    [updatedAt]      INT            NOT NULL,
    CONSTRAINT [PK_d74732762213731a98c7acce623] PRIMARY KEY CLUSTERED ([id] ASC),
    CONSTRAINT [FK_857e1cee10c832cdd99e84b5e68] FOREIGN KEY ([visualId]) REFERENCES [2ca3a77e-097c-427a-a5d3-7f3d3109902b].[visual] ([id]) ON DELETE CASCADE
);


GO

CREATE NONCLUSTERED INDEX [idx_ib_source_visualId]
    ON [2ca3a77e-097c-427a-a5d3-7f3d3109902b].[ib_source]([visualId] ASC);


GO

CREATE NONCLUSTERED INDEX [idx_ib_source_workloadItemId]
    ON [2ca3a77e-097c-427a-a5d3-7f3d3109902b].[ib_source]([workloadItemId] ASC);


GO

