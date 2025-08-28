export const getStatusSeverity = (status: string) => {
  switch (status.toLowerCase()) {
    case "running":
      return "success";
    case "queued":
      return "info";
    case "completed":
      return "success";
    case "failed":
      return "danger";
    default:
      return "warning";
  }
};

export const formatDateTime = (dateString: string | undefined) => {
  try {
    if (!dateString) {
      return "Invalid date";
    }
    const date = new Date(dateString);
    return new Intl.DateTimeFormat("en-US", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    }).format(date);
  } catch (e) {
    return "Invalid date";
  }
};

export const isJobStarted = (status: string) => {
  switch (status.toLowerCase()) {
    case "running":
      return true;
    case "queued":
      return false;
    case "completed":
      return true;
    case "cancelled":
      return true;
    case "failed":
      return true;
    default:
      return true;
  }
};

export const isJobFinished = (status: string) => {
  switch (status.toLowerCase()) {
    case "running":
      return false;
    case "queued":
      return false;
    case "completed":
      return true;
    case "cancelled":
      return true;
    case "failed":
      return true;
    default:
      return true;
  }
};
