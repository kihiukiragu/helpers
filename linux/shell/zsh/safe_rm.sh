# Add the following in ~/.zshenv (NOT ~/.zshrc) — .zshenv is sourced by
# every zsh invocation (interactive or not, login or not), while .zshrc is
# only read for interactive shells. Defining this only in .zshrc leaves the
# `rm` alias active in non-interactive shells (inherited PATH/aliases) with
# no `_safe_rm` function backing it, causing "command not found: _safe_rm".
#
# Define a function to safely delete files and directories
_safe_rm() {
  # Check if any arguments were provided
  if [[ -z "$@" ]]; then
    # If no arguments, just call the original rm (which usually prints usage)
    command rm
    return
  fi

  # The confirmation prompt below blocks on `read`, which has no one to
  # answer it when stdin isn't a real terminal — scripts, CI, and
  # tool/agent-driven shells all hang forever instead of failing or
  # deleting. In those cases there's no interactive user to protect, so
  # just run the real rm.
  if [[ ! -t 0 ]]; then
    command rm "$@"
    return
  fi

  # Determine if a recursive deletion is being attempted
  local is_recursive=false
  for arg in "$@"; do
    if [[ "$arg" == "-r" || "$arg" == "--recursive" ]]; then
      is_recursive=true
      break
    fi
  done

  # Display the items about to be deleted
  echo "You are about to delete the following items:"
  for item in "$@"; do
    # Skip printing options like -r, -f in the list of items
    # This makes the list cleaner, focusing on the actual files/directories
    if [[ "$item" != -* ]]; then
      echo "  - $item"
    fi
  done
  echo "" # Add an empty line for better readability

  # Construct the confirmation prompt message
  local confirmation_message="Are you sure you want to delete these? Type 'yes' to confirm: "
  if $is_recursive; then
    confirmation_message="WARNING: You are about to recursively delete directories and their contents.\nAre you sure? Type 'yes' to confirm: "
  fi

  # Print the prompt using printf (more robust than echo -e for prompts)
  # Then read the input separately. This avoids the 'no coprocess' error in zsh.
  printf "%b" "$confirmation_message"
  read confirm

  # Check if the user typed 'yes'
  if [[ "$confirm" == "yes" ]]; then
    # If confirmed, execute the original rm command with all arguments
    # 'command rm' ensures we call the actual rm utility and not this function recursively.
    echo "Deleting items..."
    command rm "$@"
    echo "Deletion complete."
  else
    # If not confirmed, cancel the operation
    echo "Deletion cancelled."
  fi
}

# Create an alias for 'rm' that calls our safe function
# This single alias will now handle all rm options and arguments.
alias rm='_safe_rm'
