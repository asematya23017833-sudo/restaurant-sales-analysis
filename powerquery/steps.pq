// Power Query (M) load steps
let
    Src = Csv.Document(File.Contents("data\coffee_shop_sales.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Typed = Table.TransformColumnTypes(Table.PromoteHeaders(Src),
        {{"transaction_id", Int64.Type}, {"transaction_date", type date}, {"transaction_time", type time},
         {"transaction_qty", Int64.Type}, {"unit_price", type number}}),
    WithRevenue = Table.AddColumn(Typed, "revenue", each [transaction_qty] * [unit_price], type number),
    WithHour = Table.AddColumn(WithRevenue, "hour", each Time.Hour([transaction_time]), Int64.Type)
in
    WithHour
