using SocialScoresFrontend.Components.Models;

namespace SocialScoresFrontend.Components.Infra.Session
{
    public class SessionAccountCache
    {
        public int? AccountId { get; set; }

        public void SetAccount(int accountId)
        {
            AccountId = accountId;
        }

        public bool IsLoggedIn()
        {
            return AccountId != null;
        }
    }
}
