namespace SocialScoresFrontend.Components.Models
{
    public class Account
    {
        public required int Id { get; set; }
        public required string Email { get; set; }
        public required string Username { get; set; }
        public required string Password { get; set; }
        public required int SocialScore { get; set; }

        public int? ProfileImageId { get; set; }
    }
}
