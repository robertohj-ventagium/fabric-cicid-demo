CREATE TABLE [d359507c-91ba-4dac-85a8-1c7c862bbedb].[blend_sheets] (
    [id]        NVARCHAR (128) NOT NULL,
    [name]      VARCHAR (255)  NOT NULL,
    [type]      INT            NOT NULL,
    [meta]      NVARCHAR (MAX) NOT NULL,
    [createdAt] INT            NOT NULL,
    [updatedAt] INT            NOT NULL,
    [createdBy] NVARCHAR (128) NOT NULL,
    [updatedBy] NVARCHAR (128) NOT NULL,
    CONSTRAINT [PK_blend_sheets] PRIMARY KEY CLUSTERED ([id] ASC)
);


GO

