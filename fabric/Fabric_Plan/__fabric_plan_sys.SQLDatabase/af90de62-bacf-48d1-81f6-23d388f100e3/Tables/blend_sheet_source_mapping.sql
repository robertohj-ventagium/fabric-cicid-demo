CREATE TABLE [af90de62-bacf-48d1-81f6-23d388f100e3].[blend_sheet_source_mapping] (
    [id]           INT            IDENTITY (1, 1) NOT NULL,
    [blendSheetId] NVARCHAR (128) NOT NULL,
    [sourceId]     VARCHAR (255)  NOT NULL,
    [sourceType]   INT            NOT NULL,
    [createdAt]    INT            NOT NULL,
    [updatedAt]    INT            NOT NULL,
    [createdBy]    NVARCHAR (128) NOT NULL,
    [updatedBy]    NVARCHAR (128) NOT NULL,
    CONSTRAINT [PK_blend_sheet_source_mapping] PRIMARY KEY CLUSTERED ([id] ASC),
    CONSTRAINT [FK_blend_sheet_source_mapping_blendSheetId] FOREIGN KEY ([blendSheetId]) REFERENCES [af90de62-bacf-48d1-81f6-23d388f100e3].[blend_sheets] ([id]) ON DELETE CASCADE
);


GO

CREATE NONCLUSTERED INDEX [idx_blend_sheet_source_mapping_blendSheetId]
    ON [af90de62-bacf-48d1-81f6-23d388f100e3].[blend_sheet_source_mapping]([blendSheetId] ASC);


GO

CREATE NONCLUSTERED INDEX [idx_blend_sheet_source_mapping_sourceId]
    ON [af90de62-bacf-48d1-81f6-23d388f100e3].[blend_sheet_source_mapping]([sourceId] ASC);


GO

