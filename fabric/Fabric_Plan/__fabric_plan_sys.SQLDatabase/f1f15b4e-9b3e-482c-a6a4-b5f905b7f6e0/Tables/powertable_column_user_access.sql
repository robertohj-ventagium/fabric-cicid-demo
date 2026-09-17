CREATE TABLE [f1f15b4e-9b3e-482c-a6a4-b5f905b7f6e0].[powertable_column_user_access] (
    [id]               INT            IDENTITY (1, 1) NOT NULL,
    [columnConfigId]   INT            NOT NULL,
    [accessEntityId]   VARCHAR (128)  NOT NULL,
    [accessEntityType] INT            NOT NULL,
    [permissionType]   INT            NOT NULL,
    [status]           INT            CONSTRAINT [DF_627639fbc89ec6ebf8fb60c315e] DEFAULT ((10)) NOT NULL,
    [createdBy]        NVARCHAR (128) NOT NULL,
    [updatedBy]        NVARCHAR (128) NOT NULL,
    [createdAt]        INT            NOT NULL,
    [updatedAt]        INT            NOT NULL,
    CONSTRAINT [PK_017e468771f15fc852e7e8249bd] PRIMARY KEY CLUSTERED ([id] ASC),
    CONSTRAINT [FK_7b43e70fbe0554d3ebc7f60a708] FOREIGN KEY ([columnConfigId]) REFERENCES [f1f15b4e-9b3e-482c-a6a4-b5f905b7f6e0].[powertable_column_config] ([id])
);


GO

