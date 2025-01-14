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

        public Post[] GetPostsForAccount(int accountId)
        {
            // Todo load posts for account

            return [
                new Post(){
                    Id = 1,
                    AccountId = 1,
                    Text = "Hello World",
                    User = "David",
                    TimeCreated = DateTime.Now,
                    ImageId = null
                },
                new Post(){
                    Id = 2,
                    AccountId = 1,
                    Text = "Boba kurwa",
                    User = "David",
                    TimeCreated = DateTime.Now,
                    ImageId = null
                },
            ];
        }

        private readonly BackendClient client;
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
