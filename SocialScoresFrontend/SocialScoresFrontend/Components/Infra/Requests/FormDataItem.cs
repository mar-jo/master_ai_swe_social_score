namespace SocialScoresFrontend.Components.Infra.Requests
{
    public sealed class FormDataItem
    {
        public string Name { get; init; }
        public object Value { get; init; }

        public FormDataItem(string name, object value)
        {
            this.Name = name;
            this.Value = value;
        }
    }
}
