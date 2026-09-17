
        CREATE PROCEDURE [d359507c-91ba-4dac-85a8-1c7c862bbedb].[sp_planning_di_row_values_batch_delete] 
        @InputData AS nvarchar(max),
        @DataInputRowIds AS nvarchar(max),
        @DIVTableName AS SYSNAME
        AS 
        BEGIN
        SET NOCOUNT ON;
          DECLARE @sql NVARCHAR(MAX) = '';
          DECLARE @currentTimeString NVARCHAR(50) = CONVERT(NVARCHAR(50), SYSDATETIME(), 121);
          DECLARE @TempTableName NVARCHAR(128) = '#CRV_DEL_TEMP' + REPLACE(REPLACE(REPLACE(REPLACE(@currentTimeString, '-', ''), ':', ''),' ',''),'.','');
          DECLARE @DataInputRowTempTableName NVARCHAR(128) = '#CR_DEL_TEMP' + REPLACE(REPLACE(REPLACE(REPLACE(@currentTimeString, '-', ''), ':', ''),' ',''),'.','');

          -- Create a temporary table to hold the JSON data
          SET @sql = N'
              CREATE TABLE ' + QUOTENAME(@TempTableName) + N' (
                  rowId varchar(2048) NOT NULL
              );
          ';
          
          -- Insert the incoming values into the temporary table
          SET @sql = @sql + N'
              INSERT INTO [d359507c-91ba-4dac-85a8-1c7c862bbedb].' + QUOTENAME(@TempTableName) + N'
              SELECT value as rowId FROM OPENJSON(@InputData);
          ';
      
          SET @sql = @sql + '
            DELETE [d359507c-91ba-4dac-85a8-1c7c862bbedb].' + QUOTENAME(@DIVTableName) + '
            FROM [d359507c-91ba-4dac-85a8-1c7c862bbedb].' + QUOTENAME(@DIVTableName) + '
            INNER JOIN [d359507c-91ba-4dac-85a8-1c7c862bbedb].' + QUOTENAME(@TempTableName) + ' AS temp ON temp.rowId = [d359507c-91ba-4dac-85a8-1c7c862bbedb].' + QUOTENAME(@DIVTableName) + '.rowId;';

          SET @sql = @sql + N'DROP TABLE [d359507c-91ba-4dac-85a8-1c7c862bbedb].' + @TempTableName + ';';

          -- Create a temporary table to hold the JSON data
          SET @sql = @sql + N'
            IF LEN(@DataInputRowIds) > 0
            BEGIN
            -- Create a temporary table to hold the JSON data
            CREATE TABLE ' + QUOTENAME(@DataInputRowTempTableName) + N' (
                rowId varchar(255) NOT NULL
            );

            -- Insert the incoming values into the temporary table
            INSERT INTO [d359507c-91ba-4dac-85a8-1c7c862bbedb].' + QUOTENAME(@DataInputRowTempTableName) + N'
            SELECT value as rowId FROM OPENJSON(@DataInputRowIds);

            UPDATE [d359507c-91ba-4dac-85a8-1c7c862bbedb].data_input_row SET status = 500 FROM [d359507c-91ba-4dac-85a8-1c7c862bbedb].data_input_row inner join [d359507c-91ba-4dac-85a8-1c7c862bbedb].' + @DataInputRowTempTableName + ' as temp on temp.rowId = data_input_row.id;

            DROP TABLE ' + @DataInputRowTempTableName + ';
            END
          ';

          -- Execute the dynamic SQL with the parameters passed correctly
          EXEC sp_executesql @sql, 
            N'@InputData NVARCHAR(MAX), @DataInputRowIds NVARCHAR(MAX)', 
            @InputData, 
            @DataInputRowIds;

          SET NOCOUNT OFF;
        END

GO

