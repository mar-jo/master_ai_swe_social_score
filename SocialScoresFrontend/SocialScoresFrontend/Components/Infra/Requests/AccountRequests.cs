using SocialScoresFrontend.Components.Models;

namespace SocialScoresFrontend.Components.Infra.Requests
{
    public class AccountRequests
    {
        private const string RegisterRoute = "account/register";
        private const string LoginRoute = "account/login";

        public AccountRequests(BackendClient client)
        {
            this.client = client;
        }

        public async Task<int> RegisterAccount(string username, string email, string password)
        {
            RegisterAccountContext context = new RegisterAccountContext
            {
                email = email,
                username = username,
                password = password
            };

            AccountResponse accountId = await client.Post<AccountResponse>(RegisterRoute, context);

            return accountId.id;
        }

        public async Task<int> Login(string username, string password)
        {
            LoginAccountContext context = new LoginAccountContext
            {
                username = username,
                password = password
            };

            AccountResponse accountId = await client.Post<AccountResponse>(LoginRoute, context);

            return accountId.id;
        }

        public async Task<Account> GetAccount(int id)
        {
            // ToDo route anpassen, wenn mark entwickelt hat

            return new Account()
            {
                Id = id,
                Email = "david@david.at",
                Username = "David",
                Password = "David",
                SocialScore = 2000
            };
        }

        private readonly BackendClient client;
    }

    public class LoginAccountContext
    {
        public required string username { get; set; }
        public required string password { get; set; }
    }

    public class RegisterAccountContext
    {
        public required string email { get; set; }
        public required string username { get; set; }
        public required string password { get; set; }
    }

    public class AccountResponse
    {
        public required string message { get; set; }
        public required int id { get; set; }
    }
}
