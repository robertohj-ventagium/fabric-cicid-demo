
        CREATE PROCEDURE [a9b990d3-b253-4ca7-bd42-998bde59f12b].[sp_planning_di_row_values_batch_delete] 
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
              INSERT INTO [a9b990d3-b253-4ca7-bd42-998bde59f12b].' + QUOTENAME(@TempTableName) + N'
              SELECT value as rowId FROM OPENJSON(@InputData);
          ';
      
          SET @sql = @sql + '
            DELETE [a9b990d3-b253-4ca7-bd42-998bde59f12b].' + QUOTENAME(@DIVTableName) + '
            FROM [a9b990d3-b253-4ca7-bd42-998bde59f12b].' + QUOTENAME(@DIVTableName) + '
            INNER JOIN [a9b990d3-b253-4ca7-bd42-998bde59f12b].' + QUOTENAME(@TempTableName) + ' AS temp ON temp.rowId = [a9b990d3-b253-4ca7-bd42-998bde59f12b].' + QUOTENAME(@DIVTableName) + '.rowId;';

          SET @sql = @sql + N'DROP TABLE [a9b990d3-b253-4ca7-bd42-998bde59f12b].' + @TempTableName + ';';

          -- Create a temporary table to hold the JSON data
          SET @sql = @sql + N'
            IF LEN(@DataInputRowIds) > 0
            BEGIN
            -- Create a temporary table to hold the JSON data
            CREATE TABLE ' + QUOTENAME(@DataInputRowTempTableName) + N' (
                rowId varchar(255) NOT NULL
            );

            -- Insert the incoming values into the temporary table
            INSERT INTO [a9b990d3-b253-4ca7-bd42-998bde59f12b].' + QUOTENAME(@DataInputRowTempTableName) + N'
            SELECT value as rowId FROM OPENJSON(@DataInputRowIds);

            UPDATE [a9b990d3-b253-4ca7-bd42-998bde59f12b].data_input_row SET status = 500 FROM [a9b990d3-b253-4ca7-bd42-998bde59f12b].data_input_row inner join [a9b990d3-b253-4ca7-bd42-998bde59f12b].' + @DataInputRowTempTableName + ' as temp on temp.rowId = data_input_row.id;

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

