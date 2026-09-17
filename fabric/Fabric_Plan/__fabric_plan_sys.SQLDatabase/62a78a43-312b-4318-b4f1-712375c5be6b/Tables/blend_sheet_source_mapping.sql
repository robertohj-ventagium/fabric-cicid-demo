CREATE TABLE [62a78a43-312b-4318-b4f1-712375c5be6b].[blend_sheet_source_mapping] (
    [id]           INT            IDENTITY (1, 1) NOT NULL,
    [blendSheetId] NVARCHAR (128) NOT NULL,
    [sourceId]     VARCHAR (255)  NOT NULL,
    [sourceType]   INT            NOT NULL,
    [createdAt]    INT            NOT NULL,
    [updatedAt]    INT            NOT NULL,
    [createdBy]    NVARCHAR (128) NOT NULL,
    [updatedBy]    NVARCHAR (128) NOT NULL,
    CONSTRAINT [PK_blend_sheet_source_mapping] PRIMARY KEY CLUSTERED ([id] ASC),
    CONSTRAINT [FK_blend_sheet_source_mapping_blendSheetId] FOREIGN KEY ([blendSheetId]) REFERENCES [62a78a43-312b-4318-b4f1-712375c5be6b].[blend_sheets] ([id]) ON DELETE CASCADE
);


GO

CREATE NONCLUSTERED INDEX [idx_blend_sheet_source_mapping_blendSheetId]
    ON [62a78a43-312b-4318-b4f1-712375c5be6b].[blend_sheet_source_mapping]([blendSheetId] ASC);


GO

CREATE NONCLUSTERED INDEX [idx_blend_sheet_source_mapping_sourceId]
    ON [62a78a43-312b-4318-b4f1-712375c5be6b].[blend_sheet_source_mapping]([sourceId] ASC);


GO

