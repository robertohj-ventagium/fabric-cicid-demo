CREATE TABLE [2ca3a77e-097c-427a-a5d3-7f3d3109902b].[ib_append_query_mapping] (
    [id]        INT            IDENTITY (1, 1) NOT NULL,
    [visualId]  INT            NULL,
    [sourceId]  INT            NOT NULL,
    [queryId]   INT            NOT NULL,
    [status]    INT            CONSTRAINT [DF_4b6f8c42c6efac74c8debc0e228] DEFAULT ((10)) NOT NULL,
    [createdBy] NVARCHAR (128) NOT NULL,
    [updatedBy] NVARCHAR (128) NOT NULL,
    [createdAt] INT            NOT NULL,
    [updatedAt] INT            NOT NULL,
    CONSTRAINT [PK_ce7288f7103c5778d994ef7b20f] PRIMARY KEY CLUSTERED ([id] ASC),
    CONSTRAINT [FK_655d4a8fb9e97599fb861b81cfe] FOREIGN KEY ([visualId]) REFERENCES [2ca3a77e-097c-427a-a5d3-7f3d3109902b].[visual] ([id]),
    CONSTRAINT [FK_70d1e897c99ace717e9b2014f74] FOREIGN KEY ([sourceId]) REFERENCES [2ca3a77e-097c-427a-a5d3-7f3d3109902b].[ib_source] ([id]),
    CONSTRAINT [FK_74dd35ddb1b4fbd8f776c789957] FOREIGN KEY ([queryId]) REFERENCES [2ca3a77e-097c-427a-a5d3-7f3d3109902b].[ib_queries] ([id]) ON DELETE CASCADE
);


GO

CREATE NONCLUSTERED INDEX [idx_ib_append_query_mapping_queryId]
    ON [2ca3a77e-097c-427a-a5d3-7f3d3109902b].[ib_append_query_mapping]([queryId] ASC);


GO

CREATE NONCLUSTERED INDEX [idx_ib_append_query_mapping_sourceId]
    ON [2ca3a77e-097c-427a-a5d3-7f3d3109902b].[ib_append_query_mapping]([sourceId] ASC);


GO

CREATE NONCLUSTERED INDEX [idx_ib_append_query_mapping_visualId_sourceId_queryId]
    ON [2ca3a77e-097c-427a-a5d3-7f3d3109902b].[ib_append_query_mapping]([visualId] ASC, [sourceId] ASC, [queryId] ASC);


GO

