using SocialScoresFrontend.Components.Models;

namespace SocialScoresFrontend.Components.Infra.Requests
{
    public class AccountRequests
    {
        private const string RegisterRoute = "account/register";
        private const string LoginRoute = "account/login";
        private const string GetAccountRoute = "account/info";
        private const string GetRandomAccountsRoute = "account/explore";

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
            AccountDetails details = await client.Get<AccountDetails>(GetAccountRoute + $"?account_id={id}");

            return GetAccountFromDetails(details);
        }

        public async Task<Account[]> GetRandomAccounts(int count)
        {
            AccountDetails[] details = await client.Get<AccountDetails[]>(GetRandomAccountsRoute + $"?count={count}");

            return details.Select(GetAccountFromDetails).ToArray();
        }

        private static Account GetAccountFromDetails(AccountDetails details)
        {
            return new Account()
            {
                Id = details.id,
                Email = details.email,
                Username = details.username,
                Password = details.password,
                SocialScore = details.socialscore,
                ProfileImageId = details.profile_image_id
            };
        }


        private readonly BackendClient client;
    }

    public class AccountDetails
    {
        public string password { get; set; }
        public int socialscore { get; set; }
        public int id { get; set; }
        public string email { get; set; }
        public string username { get; set; }
        public int? profile_image_id { get; set; } // Nullable integer for profile_image_id
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
