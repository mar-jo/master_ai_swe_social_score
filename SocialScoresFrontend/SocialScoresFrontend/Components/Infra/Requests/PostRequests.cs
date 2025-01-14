using SocialScoresFrontend.Components.Models;

namespace SocialScoresFrontend.Components.Infra.Requests
{
    public class PostRequests
    {
        private const string CreateNewPostRoute = "post";

        public PostRequests(BackendClient client)
        {
            this.client = client;
        }

        public async Task<CreateNewPostResponse> CreateNewPost(int accountId, string username, string text, FileData image)
        {
            FormDataItem[] formDataItems = new FormDataItem[]
            {
                new FormDataItem("user", username),
                new FormDataItem("account_id", accountId.ToString()),
                new FormDataItem("text", text),
                new FormDataItem("image", image)
            };

            return await client.PostForm<CreateNewPostResponse>(CreateNewPostRoute, formDataItems);
        }

        //public Post[] GetPostsForAccount(int accountId)
        //{
        //    // Todo load posts for account

        //    return [
        //        new Post(){
        //            Id = 1,
        //            AccountId = 1,
        //            Text = "Hello World",
        //            User = "David",
        //            TimeCreated = DateTime.Now,
        //            ImageId = null
        //        },
        //        new Post(){
        //            Id = 2,
        //            AccountId = 1,
        //            Text = "Boba kurwa",
        //            User = "David",
        //            TimeCreated = DateTime.Now,
        //            ImageId = null
        //        },
        //    ];
        //}

        public async Task<Post[]> GetPostsForAccount(int accountId)
        {
            try
            {
                PostDetail[] postDetails = await client.Get<PostDetail[]>($"account/posts?account_id={accountId}");
                return postDetails.Select(ConvertPostDetailToPost).ToArray();

            }
            catch (HttpRequestException ex)
            {
                if(ex.StatusCode == System.Net.HttpStatusCode.NotFound)
                {
                    return [];
                }

                throw;
            }
        }

        private static Post ConvertPostDetailToPost(PostDetail detail)
        {
            return new Post()
            {
                Id = detail.id,
                AccountId = detail.account_id,
                User = detail.user,
                TimeCreated = DateTime.Parse(detail.time_created),
                Text = detail.text,
                Imagedata = detail.image.data,
                MimeType = ConvertFileExtensionToMimeType(Path.GetExtension(detail.image.filename))
            };
        }

        private static string ConvertFileExtensionToMimeType(string extension)
        {
            switch (extension)
            {
                case ".png":
                    return "image/png";
                case ".jpg":
                    return "image/jpeg";
                case ".jpeg":
                    return "image/jpeg";
                default:
                    throw new ArgumentException($"Unsupported file extension {extension}");
            }
        }

        private readonly BackendClient client;
    }

    public class PostDetail
    {
        public int id { get; set; }
        public string user { get; set; }
        public int account_id { get; set; }
        public string text { get; set; }
        public string time_created { get; set; }
        public ImageDetail image { get; set; }
    }

    public class ImageDetail
    {
        public string filename { get; set; }
        public byte[] data { get; set; }
        public string uploader { get; set; }
        public string time_created { get; set; }
    }

    public class CreateNewPostResponse
    {
        public int id { get; set; }
        public string text { get; set; }
        public string time_created { get; set; }
        public int account_id { get; set; }
        public string user { get; set; }
        public int image_id { get; set; }
    }
}
