using SocialScoresFrontend.Components;
using SocialScoresFrontend.Components.Infra.Requests;
using SocialScoresFrontend.Components.Infra.Session;
using SocialScoresFrontend.Components.Infra.Utils;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

// Bootstrap communication
string? baseUrl = builder.Configuration["BackendBaseUrl"];
Assert.NotNull(baseUrl, "BackendUrl could not be found in the configuration");
builder.Services.AddHttpClient();
builder.Services.AddSingleton<BackendClient>(serviceProvider => new BackendClient(serviceProvider.GetRequiredService<HttpClient>(), baseUrl));
builder.Services.AddSingleton<AccountRequests>();
builder.Services.AddSingleton<PostRequests>();

// Session services
builder.Services.AddSingleton<SessionAccountCache>();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();

app.UseStaticFiles();
app.UseAntiforgery();

app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();

app.Run();
