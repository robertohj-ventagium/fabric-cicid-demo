CREATE TABLE [f1f15b4e-9b3e-482c-a6a4-b5f905b7f6e0].[data_input_table_metadata] (
    [id]            INT            IDENTITY (1, 1) NOT NULL,
    [tableName]     NVARCHAR (450) NOT NULL,
    [visualId]      INT            NOT NULL,
    [dimensionHash] NVARCHAR (450) NOT NULL,
    [status]        INT            CONSTRAINT [DF_66e48b7356aae8e682ae2cf361e] DEFAULT ((10)) NOT NULL,
    [createdBy]     NVARCHAR (128) NOT NULL,
    [updatedBy]     NVARCHAR (128) NOT NULL,
    [createdAt]     INT            NOT NULL,
    [updatedAt]     INT            NOT NULL,
    CONSTRAINT [PK_50ec3663f8f0eac4f89cbc6bf15] PRIMARY KEY CLUSTERED ([id] ASC),
    CONSTRAINT [FK_12867eae34e72bfd9e7af3576cb] FOREIGN KEY ([visualId]) REFERENCES [f1f15b4e-9b3e-482c-a6a4-b5f905b7f6e0].[visual] ([id])
);


GO

CREATE NONCLUSTERED INDEX [idx_data_input_table_metadata_visualId_dimensionHash]
    ON [f1f15b4e-9b3e-482c-a6a4-b5f905b7f6e0].[data_input_table_metadata]([visualId] ASC, [dimensionHash] ASC);


GO

