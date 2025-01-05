namespace SocialScoresFrontend.Components.Models
{
    public class Post
    {
        public required int Id { get; set; }
        public required int AccountId { get; set; }
        public required string User { get; set; }
        public string?Text { get; set; }
        public int? ImageId { get; set; }
        public required DateTime TimeCreated { get; set; }
    }
}
