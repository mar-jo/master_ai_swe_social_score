using SocialScoresFrontend.Components.Models;

namespace SocialScoresFrontend.Components.Infra.Requests
{
    public class PostRequests
    {
        public PostRequests(BackendClient client)
        {
            this.client = client;
        }

        public Post[] GetPostsForAccount(int accountId)
        {
            // Todo load posts for account

            return [
                new Post(){
                    Id = 1,
                    Text = "Hello World",
                    User = "David",
                    TimeCreated = DateTime.Now,
                    Image = ""
                },
                new Post(){
                    Id = 2,
                    Text = "Boba kurwa",
                    User = "David",
                    TimeCreated = DateTime.Now,
                    Image = ""
                },
            ];
        }

        private readonly BackendClient client;
    }
}
