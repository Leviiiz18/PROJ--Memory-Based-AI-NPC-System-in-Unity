using UnityEngine;
using TMPro;
using UnityEngine.Networking;
using System.Collections;
using System.Text;

public class DialogueManager : MonoBehaviour
{
    [Header("UI References")]
    public GameObject dialoguePanel;
    public TMP_Text npcText;
    public TMP_InputField playerInput;

    private string currentNPC;
    private NPCInteraction currentNPCScript;

    private bool isWaitingForResponse = false;

    void Start()
    {
        dialoguePanel.SetActive(false);
    }

    void Update()
    {
        if (!dialoguePanel.activeSelf) return;

        if (Input.GetKeyDown(KeyCode.Return) && !isWaitingForResponse)
        {
            SendMessageToNPC();
        }

        if (Input.GetKeyDown(KeyCode.Escape))
        {
            EndDialogue();
        }
    }

    public void StartDialogue(string npcName, NPCInteraction npcScript)
    {
        currentNPC = npcName;
        currentNPCScript = npcScript;

        dialoguePanel.SetActive(true);
        PlayerMovement.canMove = false;

        npcText.text = npcName + ": Hello.";
        playerInput.text = "";

        playerInput.Select();
        playerInput.ActivateInputField();
    }

    public void EndDialogue()
    {
        dialoguePanel.SetActive(false);
        PlayerMovement.canMove = true;

        if (currentNPCScript != null)
        {
            currentNPCScript.EndConversation();
        }
    }

    public void SendMessageToNPC()
    {
        if (string.IsNullOrWhiteSpace(playerInput.text)) return;
        if (isWaitingForResponse) return;

        string message = playerInput.text;
        playerInput.text = "";

        StartCoroutine(SendToBackend(message));
    }

    IEnumerator SendToBackend(string message)
    {
        isWaitingForResponse = true;

        npcText.text = currentNPC + ": Thinking...";

        string url = "http://127.0.0.1:8000/chat";

        ChatRequest data = new ChatRequest
        {
            npc_name = currentNPC,
            npc_type = "villager",
            message = message
        };

        string json = JsonUtility.ToJson(data);
        byte[] bodyRaw = Encoding.UTF8.GetBytes(json);

        UnityWebRequest request = new UnityWebRequest(url, "POST");
        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
        {
            ChatResponse response =
                JsonUtility.FromJson<ChatResponse>(request.downloadHandler.text);

            npcText.text = currentNPC + ": " + response.reply;
        }
        else
        {
            npcText.text = currentNPC + ": Cannot connect.";
            Debug.LogError(request.error);
        }

        isWaitingForResponse = false;

        playerInput.Select();
        playerInput.ActivateInputField();
    }

    [System.Serializable]
    public class ChatRequest
    {
        public string npc_name;
        public string npc_type;
        public string message;
    }

    [System.Serializable]
    public class ChatResponse
    {
        public string reply;
    }
}