namespace SocialScoresFrontend.Components.Models
{
    public class Image
    {
        public required int Id { get; set; }
        public required string FileName { get; set; }
        public required byte[] Data { get; set; }
        public required string Uploader { get; set; }
    }
}
