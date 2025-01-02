using System.Text;
using System.Text.Json;

namespace SocialScoresFrontend.Components.Infra.Requests
{
    public class BackendClient
    {
        public string BaseUrl { get; init; }

        public BackendClient(HttpClient client, string baseUrl)
        {
            _client = client;
            BaseUrl = baseUrl;
        }

        public async Task<T> Get<T>(string route)
        {
            try
            {
                var response = await _client.GetAsync($"{BaseUrl}{route}");
                response.EnsureSuccessStatusCode();
                string json = await response.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<T>(json) ?? throw new NullReferenceException();
            }
            catch (Exception ex)
            {
                // ToDo: log exception
                throw;
            }
        }

        public async Task<T> Post<T>(string route, object payload)
        {
            try
            {
                var jsonPayload = JsonSerializer.Serialize(payload);
                var content = new StringContent(jsonPayload, Encoding.UTF8, "application/json");

                var response = await _client.PostAsync($"{BaseUrl}{route}", content);
                response.EnsureSuccessStatusCode();

                string json = await response.Content.ReadAsStringAsync();
                return JsonSerializer.Deserialize<T>(json) ?? throw new NullReferenceException();
            }
            catch (Exception ex)
            {
                // ToDo: log exception
                throw;
            }
        }

        private readonly HttpClient _client;
    }
}
