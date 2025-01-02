namespace SocialScoresFrontend.Components.Models
{
    public class Post
    {
        public required int Id { get; set; }
        public required string Username { get; set; }
        public string?Text { get; set; }
        public string? Image { get; set; }
        public required DateTime TimeCreated { get; set; }
    }
}
